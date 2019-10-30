import logging
import re

from bs4 import BeautifulSoup
from selenium import webdriver


logger = logging.getLogger(__name__)


def main():
    base_url = 'https://techcrunch.com'
    url = f'{base_url}/2019/10/29/amazon-axes-14-99-amazon-fresh-fee-making-grocery-delivery-free-for-prime-members-to-boost-use/'

    try:
        soup = BeautifulSoup(get_page_source(url), 'html.parser')
    except Exception as exc:
        logger.exception(f'Unable to open page: {url}! Error: {str(exc)}')
        return None

    nav_links = get_navigation_links(soup)
    links_page_source_map = get_nav_links_page_sources(base_url, nav_links)
    write_to_file(links_page_source_map)


def get_page_source(url):
    """
    Returns the source of the page at supplied url
    :param url: string
    :return: string
    """
    browser = webdriver.Chrome('/Users/nitrix/Downloads/chromedriver')
    browser.get(url)
    return browser.page_source


def get_navigation_links(soup):
    """
    Return the navigation menu links on the page
    :param soup: BeatifulSoup instance
    :return: dict mapping navigation menu text to link
    """
    nav_menu_items_container = soup.find_all(class_='menu navigation__main-menu')[0]
    nav_items = {}
    for nav_item in nav_menu_items_container.find_all(class_='menu__item'):
        # skip all items that do not contain alphabets or numbers
        if not re.search('[a-zA-Z0-9]', nav_item.a.text):
            continue

        try:
            nav_items[nav_item.a.text] = nav_item.a['href']
        except KeyError:
            continue
    return nav_items


def get_nav_links_page_sources(base_url, nav_links):
    """
    Return the page sources for each navigation link
    :param base_url: string
    :param nav_links: dict mapping navigation menu text to link
    :return: dict mapping navigation menu text to source
    """
    nav_links_page_sources = {}
    for name, resource_path in nav_links.items():
        try:
            nav_links_page_sources[name] = get_page_source(f'{base_url}/{resource_path}')
        except Exception:
            continue

    return nav_links_page_sources


def write_to_file(links_page_source_map):
    """
    :param links_page_source_map: dict a map of the links to the page source
    :return None
    """
    for name, page_source in links_page_source_map.items():
        with open(f'{name}.html', 'w') as fp:
            fp.write(page_source)


if __name__ == '__main__':
    main()
