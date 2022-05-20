from correios import Correios, logger

logger.info('Starting buscaCEP')

initHeaders = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,es;q=0.6,la;q=0.5',
	'Content-Type': 'text/html',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
	'Origin': 'https://www2.correios.com.br',
    'Referer': 'https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm',
}
correios = Correios(initHeaders)
logger.info('Instance is set, now it\'s time to fetch records :D')
statesList = []
for state in correios.states:
	logger.info(f'Current state is: {state}')
	responseList = correios.buscaFaixaCEP(state)
	if(responseList):
		logger.info('Appending records to our final list')
		statesList.extend(responseList)
	else:
		logger.warning('Website returned status code bigger or equal to 400. We should come back later.')

logger.info('Alright, now let\'s make our records look fancy :D')
outputList = correios.listFormating(statesList)
logger.info('Writting JSONL output file...')
writeOutput = correios.writeJSONLine(outputList)
if(writeOutput == True):
	logger.info('All done!')
else:
	logger.warning('ah no! Something bad happened!')