import requests
from bs4 import BeautifulSoup


def fetch_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code != 200:
        # print(f"Failed to retrieve page {page_no} for court {court}")
        return "failed to retrieve"

    # Step 3: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def extract_data(soup, url):
    try:
        pages = 1
        # Find the pagination container
        pagination_div = soup.find('div', class_='pgbox')

        # Extract the numbers within <b> tags
        numbers = [int(b_tag.get_text()) for b_tag in pagination_div.find_all('b')]
        links = []

        if len(numbers) == 3:
            pagination_text = f"Showing {numbers[0]} to {numbers[1]} of {numbers[2]} results"
            # print(pagination_text)

            pages = numbers[2] // 10 + 1
            # print(pages)

        else:

            print("Could not find the expected number of elements in <b> tags.")

    except:

        pass

    # print(links)
    page_urls = soup.find_all('div', class_='list-code-range')
    hrefs = []
    for div in page_urls:
        links = div.find_all('a')  # Find all <a> tags in each div
        for link in links:
            if link.get('href') not in hrefs:
                hrefs.append(link.get('href'))
    # print(hrefs)

    return hrefs, pages


def main(url):
    count = 0
    urls =[]
    while True:

        if count==1:
            limit = count*10
            url = url +str(limit)
        elif count >1:
            limit = count * 10
            url = url[:-2] + str(limit)

        count = count + 1
        soup = fetch_request(url)
        links, pages = extract_data(soup, url)
        urls.extend(links)

        if pages == count:
            break


    return urls


url_links = ['https://www.aapc.com/codes/cpt-codes-range/00100-00222/', 'https://www.aapc.com/codes/cpt-codes-range/00300-00352/', 'https://www.aapc.com/codes/cpt-codes-range/00400-00474/', 'https://www.aapc.com/codes/cpt-codes-range/00500-00580/', 'https://www.aapc.com/codes/cpt-codes-range/00600-00670/', 'https://www.aapc.com/codes/cpt-codes-range/00700-00797/', 'https://www.aapc.com/codes/cpt-codes-range/00800-00882/', 'https://www.aapc.com/codes/cpt-codes-range/00902-00952/', 'https://www.aapc.com/codes/cpt-codes-range/01112-01173/', 'https://www.aapc.com/codes/cpt-codes-range/01200-01274/', 'https://www.aapc.com/codes/cpt-codes-range/01320-01444/', 'https://www.aapc.com/codes/cpt-codes-range/01462-01522/', 'https://www.aapc.com/codes/cpt-codes-range/01610-01680/', 'https://www.aapc.com/codes/cpt-codes-range/01710-01782/', 'https://www.aapc.com/codes/cpt-codes-range/01810-01860/', 'https://www.aapc.com/codes/cpt-codes-range/01916-01942/', 'https://www.aapc.com/codes/cpt-codes-range/01951-01953/', 'https://www.aapc.com/codes/cpt-codes-range/01958-01969/', 'https://www.aapc.com/codes/cpt-codes-range/01990-01999/']


final_links = []
for url in url_links:
    final_links.extend(main(url))

print(final_links)


# ['https://www.aapc.com/codes/cpt-codes-range/00100-00222/',
#  'https://www.aapc.com/codes/cpt-codes-range/00300-00352/',
#  'https://www.aapc.com/codes/cpt-codes-range/00400-00474/',
#  'https://www.aapc.com/codes/cpt-codes-range/00500-00580/',
#  'https://www.aapc.com/codes/cpt-codes-range/00600-00670/',
#  'https://www.aapc.com/codes/cpt-codes-range/00700-00797/',
#  'https://www.aapc.com/codes/cpt-codes-range/00800-00882/',
#  'https://www.aapc.com/codes/cpt-codes-range/00902-00952/',
#  'https://www.aapc.com/codes/cpt-codes-range/01112-01173/',
#  'https://www.aapc.com/codes/cpt-codes-range/01200-01274/']
