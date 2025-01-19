import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def fetch_and_save(url, depth, output_dir):
    if depth < 0:
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 設置會話與重試機制
        session = requests.Session()
        retry_strategy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[403, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # 替代 method_whitelist
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        # 發送請求
        response = session.get(url, headers=headers)
        response.raise_for_status()

        # 解析並保存網頁
        soup = BeautifulSoup(response.text, 'html.parser')
        filename = os.path.join(output_dir, url.replace('http://', '').replace('https://', '').replace('/', '_') + '.html')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        print(f"Saved: {filename}")

        # 遞迴抓取
        if depth > 0:
            links = {urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)}
            for link in links:
                if link.startswith('http'):
                    fetch_and_save(link, depth - 1, output_dir)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Retrieve website content to a specified depth.")
    parser.add_argument('url', type=str, help="The starting URL")
    parser.add_argument('depth', type=int, help="Depth of crawling")
    parser.add_argument('output_dir', type=str, help="Directory to save the files")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    fetch_and_save(args.url, args.depth, args.output_dir)
