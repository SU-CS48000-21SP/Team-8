from html.parser import HTMLParser
from bs4 import BeautifulSoup

def parse_code(body):
        body = body.replace("&gt","")
        parsed_html = BeautifulSoup(body, features="lxml")
        code = parsed_html.body.find_all('code')
        str_code = str(code)
        str_code = str_code.replace(',', '')
        str_code = str_code.replace('\n', '')
        str_code = str_code.replace('"', '')
        str_code = str_code.replace(' ', '')
        str_code = str_code.replace(';', '')
        return str_code

def parse_body(body):
        parsed_html = BeautifulSoup(body, features="lxml")
        text = parsed_html.get_text()
        text = text.replace(',', '')
        text = text.replace('\n', '')
        text = text.replace('"', '')
        return text

