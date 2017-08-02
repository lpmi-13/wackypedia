from bs4 import BeautifulSoup
import re, requests, os

wiki_prefix = 'https://en.wikipedia.org'
file_path = 'data/'
seed_url = 'https://en.wikipedia.org/wiki/Biomedical_sciences'

seed_page = requests.get(seed_url)
text = BeautifulSoup(seed_page.content, 'html.parser')

urls = text.find_all('a', href=re.compile('^/wiki/'))

# strip out links with colons, since these are things like template pages
links = (url['href'] for url in urls if ':' not in url['href'])

for link in links:

    secondary_page = requests.get(wiki_prefix + link)
    secondary_html = BeautifulSoup(secondary_page.content, 'html.parser')
    # the content we want is all inside the p tags
    content = secondary_html.find_all('p')

    paragraph_text = ''

    for paragraph in content:

        paragraph_text += paragraph.getText()

    print('creating file for', link[6:])
    file_name = link[6:]
    with open(file_path + file_name + '.txt', 'w') as page_file:
        page_file.write(paragraph_text)
        
        
