import json

from tqdm import tqdm
import os
import requests
import mimetypes
from multiprocessing import Pool, cpu_count
from functools import partial
import logging
from typing import List
import random
import time

mimetypes.init()
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler('image_dl.log', mode='a')])

IMAGE_TYPES = [i for i in mimetypes.types_map.values() if 'image' in i]


def _download(url: str, dest_folder: str, filename=None, check_content_type=True):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder, exist_ok=True)  # create folder if it does not exist
    if filename is None:
        filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)
    try:
        r = requests.get(url, stream=True, timeout=10)
    except requests.exceptions.ConnectionError as e:
        logging.error(f'Download for {url} failed - {e}\nDoes website exist?')
        return 0
    if r.status_code == 200:
        if check_content_type:
            content_type = r.headers.get('Content-Type', 'NONE')
            if content_type not in IMAGE_TYPES:
                logging.error(
                    f"Download for {url} failed: content type {r.headers.get('Content-Type')} not in image types")
                return 0
            expected_ext = mimetypes.types_map.get(content_type, '.jpg')
            if not file_path.endswith(expected_ext):
                file_path += expected_ext
        with open(file_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        return 1
    else:  # HTTP status code 4XX/5XX
        logging.error(f"Download for {url} failed: status code {r.status_code}")
        return 0


def download(url_list: List[str], dest_folder: str, workers=None, check_content_type=True):
    if workers is None:
        workers = cpu_count() * 8
    with Pool(workers) as p:
        for _ in tqdm(
                p.imap_unordered(partial(_download, dest_folder=dest_folder, check_content_type=check_content_type),
                                 url_list), desc='Downloading '
                                                 'images...'):
            pass

def random_valid_url(min_size=100, max_size=1000):
    return f'https://lorempixel.com/{random.randint(min_size, max_size)}/' \
                f'{random.randint(min_size, max_size)}'

def test_download(n=1000, workers=None):
    url_list = [random_valid_url() for _ in range(n)]
    fake_urls = [f'https://randomwebsitejhsakj{random.randint(0, 100):04}.com/image.jpg' for _ in range(10)]
    url_list += fake_urls
    random.shuffle(url_list)
    download(url_list, 'test_out', check_content_type=True, workers=workers)


if __name__ == "__main__":
    results = {}
    for i in range(1, 50, 5):
        start = time.time()
        print(f'\n\nTESTING N PROCESSES = {i}\n\n')
        test_download(workers=i)
        total = time.time() - start
        results[i] = total
    with open('speed_test_results.json', 'w') as f:
        json.dump(results, f, indent=4)