# Third-Party Imports
import requests as r
from bs4 import BeautifulSoup
# Standard Library Imports
import re
import os
from sys import argv
# Local Imports
from queries import get_text_cli

def search(term, advanced_parse=False):
    base_url = "https://en.wikipedia.org/wiki/"
    res = r.get(base_url + term)

    if res.status_code == 200:
        return parser(res.text, advanced_parse)
    
    return None

def parser(text, advanced=False):
    soup = BeautifulSoup(text, "html.parser")
    title = soup.title.text.replace("- Wikipedia", "").strip()
    page_id = soup.find(id="t-wikibase").a.attrs['href'].split("/")[-1]
    main_content = soup.find(id="bodyContent")

    if advanced:
        main_content.find(id="toc").decompose()
        main_content.find(id="catlinks").decompose()
        main_content.find(id="References").decompose()
        reference_list = main_content.find_all(attrs={"class": "reflist"})[-1]

        for sibling in reference_list.find_next_siblings():
            sibling.decompose()

        reference_list.decompose()

        for foot in main_content.find_all(attrs={"class": "printfooter"}):
            foot.decompose()
    
        content_string = main_content.get_text()
    else:
        content_string = ""
        for paragraph in main_content.find_all("p"):
            content_string += paragraph.get_text()
    
    content_string = re.sub("\\[([0-9]*?)\\]", "", content_string)
    return page_id, title, content_string.strip()

def save_article(page_info, directory="corpus"):
    main_path = os.path.join(os.path.dirname(__file__), directory)
    if any(page_info[0] in file for file in os.listdir(main_path)):
        print("Article already exists in corpus")
        return

    file_name = f"{page_info[0]}-{page_info[1]}.txt"

    with open(os.path.join(main_path, file_name), "w") as f:
        f.write(page_info[2])

if __name__ == "__main__":
    search_term = get_text_cli("Enter a search term", min_length=1)
    search_result = search(search_term)
    save_article(search_result)