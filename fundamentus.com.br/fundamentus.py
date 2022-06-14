"""
Fundamentus is a free website that provides information about the Brazilian stock market (BVMF).
"""
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from time import time
import aiohttp
from bs4 import BeautifulSoup

OUTPUT_DIR = './output'
FUNDAMENTUS_URL = 'https://fundamentus.com.br/resultado.php?setor=%s'
REQUEST_HEADERS = [('connection', 'keep-alive'), ('authority', 'fundamentus.com.br'), ('cache-control', 'max-age=0'),('sec-ch-ua', '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"'), ('sec-ch-ua-mobile', '?0'), ('upgrade-insecure-requests', '1'), ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'), ('sec-fetch-site', 'none'), ('sec-fetch-mode', 'navigate'), ('sec-fetch-user', '?1'), ('sec-fetch-dest', 'document'), ('accept-language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'), ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_output_dir():
    """ Create the output dir, if it does not exist. """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_data_from(html):
    """ Extract, from the html page, a dictionary with the financial data.
        :param html: content of html page
    """
    soup = BeautifulSoup(html)
    thead, tbody = soup.findAll('thead'), soup.findAll('tbody')
    if len(thead) == 0 or len(tbody) == 0:
        return {'error' : 'invalid thead/tbody'}

    htrs, btrs = thead[0].findAll('tr'), tbody[0].findAll('tr')
    if len(htrs) == 0 or len(btrs) == 0:
        return {'error' : 'invalid thead.tr/tbody.tr'}

    ths, tds = htrs[0].findAll('th'), btrs[0].findAll('td')
    result = {}
    for i, th in enumerate(ths):
        result[th.text.strip()] = tds[i].text.strip()
    return result

def write_to_json_file(sector_id, dict_data):
    """ Write the dictionary data to a JSON file.
        :param sector_id: id of a financial sector
        :param dict_data: dictonary with the data
    """
    if not dict_data:
        return

    today = datetime.now().strftime('%Y%m%d')
    filename = f'{OUTPUT_DIR}/sector_{sector_id}_{today}.json'
    if dict_data.get('error'):
        filename += '.error'

    with Path(filename).open('w', encoding='utf8') as f:
        f.write(json.dumps(dict_data))

async def get_sector_data(session, sector_id):
    """ Asynchronously download data from a financial sector.
        :param sector_id: id of a financial sector
    """
    link = FUNDAMENTUS_URL % sector_id
    async with session.get(link) as resp:
        data = await resp.read()
    write_to_json_file(sector_id, extract_data_from(data))
    logger.info('Downloaded data from %s', sector_id)

async def main():
    """ Downloads financial data from 50 industries of Bovespa """
    sector_ids = range(1, 51)
    async with aiohttp.ClientSession(headers=REQUEST_HEADERS) as session:
        tasks = [(get_sector_data(session, sector_id)) for sector_id in sector_ids]
        await asyncio.gather(*tasks, return_exceptions=False)

if __name__ == '__main__':
    ts = time()
    setup_output_dir()
    asyncio.new_event_loop().run_until_complete(main())
    logger.info('Took %s seconds to complete', time() - ts)
