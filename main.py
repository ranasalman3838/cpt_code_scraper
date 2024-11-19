import requests
from bs4 import BeautifulSoup
import concurrent.futures
import logging
from urllib.parse import urlparse




# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_page():
    # Step 1: Set up the URL with dynamic page number and year
    # urls = [
    # "https://www.aapc.com/codes/cpt-codes-range/00100-01999/",
    # "https://www.aapc.com/codes/cpt-codes-range/10004-69990/",
    # "https://www.aapc.com/codes/cpt-codes-range/70010-79999/",
    # "https://www.aapc.com/codes/cpt-codes-range/80047-89398/",
    # "https://www.aapc.com/codes/cpt-codes-range/90281-99607/",
    # "https://www.aapc.com/codes/cpt-codes-range/99091-99499/",
    # "https://www.aapc.com/codes/cpt-codes-range/0001F-9007F/",
    # "https://www.aapc.com/codes/cpt-codes-range/0002M-0020M/",
    # "https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/",
    # "https://www.aapc.com/codes/cpt-codes-range/0001U-0520U/",
    # "https://www.aapc.com/codes/cpt-codes-range/cpt-modifiers/"
    # ]
    urls = ['https://www.aapc.com/codes/cpt-codes-range/00100-01999/']

    # urls = ['https://www.aapc.com/codes/cpt-codes-range/00100-00222/']

    for url in urls:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }

        try:
            # Step 2: Send a request to the page with headers
            response = requests.get(url, headers=headers)

            # Check if the response is successful
            if response.status_code != 200:
                # print(f"Failed to retrieve page {page_no} for court {court}")
                return "failed to retrieve"

            # Step 3: Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            links = [url]

            try:
                # Find the pagination container
                pagination_div = soup.find('div', class_='pgbox')

                # Find all anchor tags within the pagination container
                # pagination_links = pagination_div.find_all('a')
                # Extract the numbers within <b> tags
                numbers = [int(b_tag.get_text()) for b_tag in pagination_div.find_all('b')]

                if len(numbers) == 3:
                    pagination_text = f"Showing {numbers[0]} to {numbers[1]} of {numbers[2]} results"
                    print(pagination_text)

                    pages =numbers[2]//10 + 1
                    print(pages)

                    for i in range(1, pages):
                        limit = i*10
                        new_url = f"{url}{limit}"
                        links.append(new_url)

                else:
                    print("Could not find the expected number of elements in <b> tags.")

            except Exception as e:
                print(f"Could not find pagination links: {e}")

            print(links)
            page_urls = soup.find_all('div', class_='list-code-range')
            hrefs = []
            for div in page_urls:
                links = div.find_all('a')  # Find all <a> tags in each div
                for link in links:
                    if link.get('href') not in hrefs:
                        hrefs.append(link.get('href'))
            print(hrefs)

            # # Step 5: Locate all <a> tags with class 'modern-card-table__link' and extract their href attributes
            # links = soup.find_all('a', class_='modern-card-table__link')
            # hrefs = [link.get('href') for link in links]
            #
            # # Step 6: Append the hrefs to the file (create file if it doesn't exist)
            # file_name = f"hrefs_{year}_batch3.txt"
            # with open(file_name, "a") as f:
            #     for href in hrefs:
            #         f.write(f"{href}\n")
            #
            # logging.info(f"Scraped court {court}, page {page_no}, year {year}")
            #
            # # Step 7: Return the pagination info
            # return pagination_info

        except Exception as e:
            # logging.error(
            #     f"Error on page {page_no} of court {court}, year {year}: {str(e)}")
            # # Log the error to url_errors.txt
            # with open(f'url_errors_batch3_{year}.txt', 'a') as error_file:
            #     error_file.write(
            #         f"Error on page {page_no} of court {court}, year {year}: {str(e)}\n")

            # Return None if there's an error, so we stop pagination
            return None

scrape_page()



urls_list_section = {
    "Anesthesia" : ['https://www.aapc.com/codes/cpt-codes-range/00100-01999/', 'https://www.aapc.com/codes/cpt-codes-range/00100-01999/10'],
    "Surgery": ['https://www.aapc.com/codes/cpt-codes-range/10004-69990/', 'https://www.aapc.com/codes/cpt-codes-range/10004-69990/10'],
    "Radiology Procedures" : ['https://www.aapc.com/codes/cpt-codes-range/70010-79999/'],
    "Pathology and Laboratory Procedures" : ['https://www.aapc.com/codes/cpt-codes-range/80047-89398/', 'https://www.aapc.com/codes/cpt-codes-range/80047-89398/10', 'https://www.aapc.com/codes/cpt-codes-range/80047-89398/20'],
    "Medicine Services and Procedures": ['https://www.aapc.com/codes/cpt-codes-range/90281-99607/', 'https://www.aapc.com/codes/cpt-codes-range/90281-99607/10', 'https://www.aapc.com/codes/cpt-codes-range/90281-99607/20', 'https://www.aapc.com/codes/cpt-codes-range/90281-99607/30'],
    "Evaluation and Management": ['https://www.aapc.com/codes/cpt-codes-range/99091-99499/', 'https://www.aapc.com/codes/cpt-codes-range/99091-99499/10', 'https://www.aapc.com/codes/cpt-codes-range/99091-99499/20'],
    "Category II Codes": ['https://www.aapc.com/codes/cpt-codes-range/0001F-9007F/'],
    "Multianalyte Assay": ['https://www.aapc.com/codes/cpt-codes-range/0002M-0020M/', 'https://www.aapc.com/codes/cpt-codes-range/0002M-0020M/10'],
    "Category III Codes": ['https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/10', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/20', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/30', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/40', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/50', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/60', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/70', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/80', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/90', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/100', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/110', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/120', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/130', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/140', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/150', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/160', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/170', 'https://www.aapc.com/codes/cpt-codes-range/0042T-0900T/180'],
}