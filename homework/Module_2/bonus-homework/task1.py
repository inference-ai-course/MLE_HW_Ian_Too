import requests, time, json
from bs4 import BeautifulSoup
import trafilatura
from selenium import webdriver
from PIL import Image
import pytesseract
from io import BytesIO

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_search_results(start: int, category: str) -> str:
    """
    Fetches the HTML content of arXiv search results for a given category and start index.
    """
    # Use a general query that will return papers from the category
    query = "computer science" if category == "computer_science" else "artificial intelligence"
    url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&order=-announced_date_first&size=50&start={start}"
    response = requests.get(url, headers=HEADERS)
    return response.text

def parse_search_page(html: str) -> list:
    """
    Parses the search results page and extracts /abs/ URLs of individual papers.
    """
    soup = BeautifulSoup(html, 'html.parser')
    papers = soup.find_all('li', class_='arxiv-result')
    urls = []
    for p in papers:
        try:
            link = p.find('p', class_='list-title').find('a')['href']
            # Convert relative URLs to absolute
            if link.startswith('/'):
                link = 'https://arxiv.org' + link
            urls.append(link)
        except (AttributeError, KeyError) as e:
            print(f"Error parsing paper link: {e}")
            continue
    return urls

def scrape_abs_page(url: str) -> dict:
    """
    Scrapes metadata from an arXiv /abs/ page: title, authors, abstract, and date.
    """
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1', class_='title').text.replace('Title:', '').strip()
    authors = [a.text for a in soup.find('div', class_='authors').find_all('a')]
    abstract = soup.find('blockquote', class_='abstract').text.replace('Abstract:', '').strip()
    date = soup.find('div', class_='dateline').text.strip()
    return {'url': url, 'title': title, 'authors': authors, 'abstract': abstract, 'date': date}

def clean_abstract_with_trafilatura(url: str) -> str:
    """
    Uses Trafilatura to clean and extract readable abstract text from the /abs/ page.
    """
    downloaded = trafilatura.fetch_url(url)
    return trafilatura.extract(downloaded)

def extract_abstract_with_ocr(url: str) -> str:
    """
    Uses Selenium and Tesseract OCR to extract abstract text from a screenshot of the /abs/ page.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    image = Image.open(BytesIO(screenshot))
    return pytesseract.image_to_string(image)

def save_to_json(data: list, filename: str):
    """
    Saves the scraped data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main_scraper(category: str = "computer_science", max_papers: int = 200):
    """
    Main function to scrape abstracts from arXiv for a given category and number of papers.
    """
    results = []
    print(f"Starting to scrape {max_papers} papers from {category} category...")
    
    for start in range(0, max_papers, 50):
        print(f"Fetching batch starting at {start}...")
        try:
            html = fetch_search_results(start, category)
            urls = parse_search_page(html)
            print(f"Found {len(urls)} papers in this batch")
            
            for i, url in enumerate(urls):
                if len(results) >= max_papers:
                    break
                    
                try:
                    print(f"Scraping paper {len(results)+1}/{max_papers}: {url}")
                    paper = scrape_abs_page(url)
                    
                    # Try trafilatura first, fallback to original abstract
                    clean = clean_abstract_with_trafilatura(url)
                    if clean and len(clean.strip()) > 50:  # Only use if substantial content
                        paper['abstract'] = clean
                    # Keep original abstract if trafilatura doesn't work well
                    
                    results.append(paper)
                    time.sleep(1)  # Be respectful to the server
                    
                except Exception as e:
                    print(f"Error scraping {url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching batch at {start}: {e}")
            continue
            
        if len(results) >= max_papers:
            break
    
    print(f"Scraped {len(results)} papers total")
    save_to_json(results, f'arxiv_{category}_abstracts.json')
    print(f"Saved results to arxiv_{category}_abstracts.json")
