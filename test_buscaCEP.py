from unittest import mock
import unittest
from correios import Correios


def loadPageHTML(page: int) -> str:
        if(page == 1):
            with open('examples/firstPage.html', 'r') as f:
                firstPage = f.read()
                f.close()
            return firstPage
        if(page > 1):
            with open('examples/n-thPage.html', 'r') as f:
                nthPage = f.read()
                f.close()
            return nthPage

class TestCorreios(unittest.TestCase):

    def setUp(self):
        print('Setting up enviroment variables')
        self.state = 'AL'
        self.initHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,es;q=0.6,la;q=0.5',
        'Content-Type': 'text/html',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        'Origin': 'https://www2.correios.com.br',
        'Referer': 'https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm',
        }
        self.data = {
		'UF': self.state,
		'Localidade': '',
		'Bairro': '',
		'qtdrow': 50,
		'pagini': 1,
		'pagfim': 50
		}
        self.correios = Correios(self.initHeaders)
    
    @mock.patch.object(Correios, 'buscaFaixaCEP', return_value = list())
    def test_external_request(self, a):
        externalCall = self.correios.buscaFaixaCEP(self.state)
        self.assertIsInstance(externalCall, list)
    
    @mock.patch.object(Correios, '_buscaResultado', return_value = tuple())
    def test_internal_request(self, b):
        self.assertIsInstance(self.correios._buscaResultado(self.data), tuple)
    
    @mock.patch.object(Correios, 'listFormating', return_value=list())
    def test_list_formatting(self, c):
        listFormatting = self.correios.listFormating(self.state)
        self.assertIsInstance(listFormatting, list)
    
    @mock.patch.object(Correios, 'writeJSONLine', return_value= bool())
    def test_writting_jsonl(self, d):
        writtingJSONL = self.correios.writeJSONLine(list())
        self.assertIsInstance(writtingJSONL, bool)

    @mock.patch.object(Correios, '_extractHTMLTable', return_value = loadPageHTML(1))
    def test_extractHTMLTable(self, e):
        self.assertIsInstance(self.correios._extractHTMLTable(), str)

    @mock.patch.object(Correios, '_extractHTMLTableIter', return_value = loadPageHTML(2))
    def test_extractHTMLTableIter(self, e):
        self.assertIsInstance(self.correios._extractHTMLTableIter(), str)
        
    @mock.patch.object(Correios, '_extractPages', return_value = tuple())
    def test_extractPages(self, f):
        self.assertIsInstance(self.correios._extractPages(), tuple)

    @mock.patch.object(Correios, '_extractStates', return_value = tuple())
    def test_extractPages(self, f):
        self.assertIsInstance(self.correios._extractStates(), tuple)

    @mock.patch.object(Correios, '_cleanEmptyElements', return_value = list())
    def test_cleanEmptyElements(self, g):
        self.assertIsInstance(self.correios._cleanEmptyElements(), list)
    
    @mock.patch.object(Correios, '_structureList', return_value = list())
    def test_structureList(self, h):
        self.assertIsInstance(self.correios._structureList(), list)

    @mock.patch.object(Correios, '_removeDuplicatesFromList', return_value = list())
    def test_removeDuplicatesFromList(self, j):
        self.assertIsInstance(self.correios._removeDuplicatesFromList(), list)

    @mock.patch.object(Correios, '_generateListIdentifier', return_value = list())
    def test_generateListIdentifier(self, k):
        self.assertIsInstance(self.correios._generateListIdentifier(), list)

    @mock.patch.object(Correios, '_mergeDictionaries', return_value = dict())
    def test_mergeDictionaries(self, l):
        self.assertIsInstance(self.correios._mergeDictionaries(), dict)

    def tearDown(self):
        print('time to tearDown')


if __name__ ==  '__main__':
    unittest.main()