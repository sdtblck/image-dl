# image-dl

A fast and straightforward image downloader in python using multiprocessing + requests

## Example usage:

```python
from image_dl import download, random_valid_url

url_list = [random_valid_url() for _ in range(100)]
download(url_list, 'images') # list of urls / destination folder
```