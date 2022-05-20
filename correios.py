
import requests, html_to_json, jsonlines, logging
from scrapy import Selector

logger = logging.getLogger('Correios WEB CRAWLER')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

class Correios():
	def __init__(self, initHeaders: dict) -> object:
		self._headers = initHeaders
		#Initializing session and using cookies for later requests :D
		logger.info('Initializing session on buscaFaixaCep.cfm page.')
		self.s = requests.Session()
		initRequest = self.s.get('https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm', headers=self._headers)
		logger.info('Extracting all states from html page.')
		self.states = self._extractStates(initRequest.content)

	def _convertHTMLTableToList(self, html: str) -> list:
		self._html = html
		rawList = html_to_json.convert_tables(self._html)
		logger.info('Cleaning up empty records...')
		cleanEmptyElements = self._cleanEmptyElements(rawList)

		return cleanEmptyElements
	
	def _convertHTMLTableToListIter(self, html: str) -> list:
		self._html = html
		rawList = html_to_json.convert_tables(self._html)
		cleanEmptyElements = self._cleanEmptyElements(rawList)
		preparedList = [list(element.values()) for element in cleanEmptyElements]

		return preparedList

	def _cleanEmptyElements(self, rawList: list) -> list:
		self._rawList = rawList
		cleanList = [element for element in self._rawList[0] if element]

		return cleanList

	def _extractHTMLTable(self, html: str) -> str:
		self._html = html
		sel = Selector(text=self._html, type='html')
		table = sel.xpath("/html/body/div[@class='back']/div[@class='tabs']/div[@class='wrap'][2]/div[@class='content']/div[@class='laminas']/div[@class='column2']/div[@class='content ']/div[@class='ctrlcontent']/table[@class='tmptabela'][2]").extract()
		return table[0]

	def _extractHTMLTableIter(self, html: str) -> str:
		self._html = html
		sel = Selector(text=self._html, type='html')
		table = sel.xpath("/html/body/div[@class='back']/div[@class='tabs']/div[@class='wrap'][2]/div[@class='content']/div[@class='laminas']/div[@class='column2']/div[@class='content ']/div[@class='ctrlcontent']/table[@class='tmptabela'][1]").extract()
		return table[0]
	
	def _extractPages(self, html: str) -> tuple:
		self._html = html
		sel = Selector(text=self._html, type='html')
		pagesText = sel.xpath("/html/body/div[@class='back']/div[@class='tabs']/div[@class='wrap'][2]/div[@class='content']/div[@class='laminas']/div[@class='column2']/div[@class='content ']/div[@class='ctrlcontent']/br/preceding::text()[1]").extract()
		pages = tuple([int(integer) for integer in pagesText[0].strip().split(' ') if integer.isdigit()])
		return pages
	
	def _extractStates(self, html: str) -> list:
		self._html = html
		sel = Selector(text=self._html, type='html')
		statesSelect = sel.xpath("/html/body/div[@class='back']/div[@class='tabs']/div[@class='wrap'][2]/div[@class='content']/div[@class='laminas']/div[@class='column2']/div[@class='content ']/div[@class='ctrlcontent']/form[@id='Geral']/div[@class='form']/div[@class='contentform']/span[2]/label/select[@class='f1col']").extract()
		dictStates = html_to_json.convert(statesSelect[0], capture_element_attributes=False)
		states = [state['_value'] for state in dictStates['select'][0]['option'] if state]
		return states

	def buscaFaixaCEP(self, state: str) -> list:
		self._state = state
		self._data = {
		'UF': self._state,
		'Localidade': '',
		'Bairro': '',
		'qtdrow': 50,
		'pagini': 1,
		'pagfim': 50
		}
		logger.info('Fetching records from first page...')
		response, status = self._buscaResultado(data=self._data)
		if(status == True):
			logger.info('OK! Let\'s extract the HTML table from the first page now')
			table = self._extractHTMLTable(response)
			logger.info('Extracting how many records are available to fetch...')
			startPage, endPage, maxElements = self._extractPages(response)
			logger.info(f'Extraction found a total of {maxElements} records!')
			logger.info('Converting HTML table to a list...')
			tableList = self._convertHTMLTableToList(table)
			iterStartPage = endPage
			while(iterStartPage < maxElements):
				logger.info('Wait! There is more records we need to fetch :D')
				self._data['pagini'] = iterStartPage + 1,
				self._data['pagfim'] = iterStartPage + 50
				logger.info(f'Next POST payload will be including pagini: {self._data["pagini"]} and pagfim: {self._data["pagfim"]}')
				logger.info(f'Fetching new records...')
				iterResponse, iterStatus = self._buscaResultado(data=self._data)
				if(iterStatus == True):
					logger.info('OK! Let\'s extract the HTML table from this new page now')
					iterTable = self._extractHTMLTableIter(iterResponse)
					iterStartPage, iterEndPage, iterMaxElements = self._extractPages(iterResponse)
					logger.info('Converting HTML table to a list...')
					itertableList = self._convertHTMLTableToListIter(iterTable)
					iterStartPage = iterEndPage
					logger.info('Appending records to list...')
					tableList.extend(itertableList)			
			return tableList
		return []

	def _buscaResultado(self, data: dict) -> tuple():
		self._data = data
		response = self.s.post('https://www2.correios.com.br/sistemas/buscacep/ResultadoBuscaFaixaCEP.cfm', data=self._data)

		return response.text, response.ok

	def _structureList(self, list: list) -> list:
		self._list = list
		structuredList = [{"localidade": element[0], "faixaCEP": element[1].strip()} for element in self._list if element[3] == "Total do município"]

		return structuredList

	def _removeDuplicatesFromList(self, list: list) -> list:
		self._list = list
		removeDuplicates = [i for n, i in enumerate(self._list ) if i not in self._list[n + 1:]]

		return removeDuplicates

	def _generateListIdentifier(self, list: list) -> list:
		self._list = list
		addIdentifier = [self._mergeDictionaries({"id":id + 1}, dictionary) for id, dictionary in enumerate(self._list)]
		
		return addIdentifier

	def _mergeDictionaries(self, dict1: dict, dict2: dict) -> dict:
		self._dict1 = dict1
		self._dict2 = dict2

		return {**self._dict1, **self._dict2}

	def writeJSONLine(self, list: list) -> bool:
		self._list = list
		file = 'output.jsonl'
		try:
			with jsonlines.open(file, 'w') as writer:
				writer.write_all(self._list)
				writer.close()
			return True
		except:
			return False

	def listFormating(self, responseList: list) -> list:
		self._list = responseList
		logger.info('Structuring records to match requirements')
		structuredList = self._structureList(self._list)
		logger.info('Removing duplicate records from list')
		removeDuplicates = self._removeDuplicatesFromList(structuredList)
		logger.info('Assigning unique id to records')
		addIdentifier = self._generateListIdentifier(removeDuplicates)
		return addIdentifier