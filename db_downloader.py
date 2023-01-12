# Download the database from the server if it doesn't already exist
from tqdm import tqdm
import os
import zipfile
import urllib.request

URL = 'https://nationalpooling.com/reports/region/AllBlocksAugmentedReport.zip'

def download_and_extract(file_name, url=URL):
    if not os.path.exists(file_name):
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=file_name) as t:
            urllib.request.urlretrieve(url, 'AllBlocksAugmentedReport.zip', reporthook=lambda count, block_size, total_size: t.update((block_size*count)))
        with zipfile.ZipFile('AllBlocksAugmentedReport.zip', 'r') as zip_ref:
            zip_ref.extractall()
        os.remove('AllBlocksAugmentedReport.zip')
        os.rename('AllBlocksAugmentedReport.txt', 'phone_numbers.csv')
    else:
        pass