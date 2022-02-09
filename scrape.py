import requests
import re
import os
import itertools as it
from dateutil import parser
from collections import defaultdict
from lxml import etree

date_format = r"(?:'?\d{1,4}(?:th|nd|st)?[\s,]+)*(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:ril)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:[\s,]+'?\d{1,4}(?:th|nd|st)?)*"

valueserp_url = 'https://api.valueserp.com/search'
valueserp_params = {
    'api_key': os.environ['VALUESERP_API_KEY'],
    'gl': 'br',
    'hl': 'pt',
    'location': 'State of Rio de Janeiro,Brazil',
    'google_domain': 'google.com.br'
}

def search(txt):
    params = {
       **valueserp_params,
       'q': txt
    }

    api_result = requests.get(valueserp_url, params)
    assert api_result.ok

    return api_result.json()

def dict_leaves(d):
    if type(d) is str:
        yield d
    elif type(d) is list:
        for elem in d:
            yield from dict_leaves(elem)
    elif type(d) is dict:
        for v in d.values():
            yield from dict_leaves(v)

def text_answers(api_response, max=10):
    if 'answer_box' in api_response:
        for answer in api_response['answer_box']['answers']:
            yield from dict_leaves(answer['answer'])
    
    for result in api_response['organic_results'][:max]:
        yield result['snippet']

def url_answers(api_response):
    for result in api_response['organic_results']:
        yield result['link']

def find_date(txt, tol=3):
    """Find a date online using a text query and return a datetime object"""

    api_response = search(txt)
    dates = it.chain(*(re.findall(date_format, answer) for answer in text_answers(api_response, max=tol)))
    try:
        return parser.parse(next(dates))
    except StopIteration:
        return None

def find_site(txt):
    """Find a website online using a text query and return an html string"""

    api_response = search(txt)
    urls = url_answers(api_response)
    url = next(urls)
    page_response = requests.get(url)
    assert page_response.ok
    return page_response.text

def list_leaves(page):
    for node in page.iter('*'):
        if len(node) > 0:
            # skip non-leaves
            continue

        if not node.text:
            # skip empty leaves
            continue

        yield node

def generic_xpath(xpath):
    return re.sub('\[\d+\]|/a', '', xpath)

def find_sequences(site):
    page = etree.HTML(site).xpath('//html/body')[0]
    tree = etree.ElementTree(page)
    sequences = defaultdict(list)

    for leaf in list_leaves(page):
        xpath = tree.getpath(leaf)
        text = leaf.text.strip()
        if text and 'script' not in xpath:
            gxpath = generic_xpath(xpath)
            sequences[gxpath].append(text)

    return list(sequences.values())