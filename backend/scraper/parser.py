from bs4 import BeautifulSoup


def parse_html(html: str) -> BeautifulSoup:
    """HTMLをBeautifulSoupで解析する"""
    return BeautifulSoup(html, 'html.parser')