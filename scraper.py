import requests
import string
import os

from bs4 import BeautifulSoup
from urllib.parse import urlparse


def remove_punctuation(my_string):
    punctuation = string.punctuation
    for c in punctuation:
        my_string = my_string.replace(c, '', 10)

    my_string = my_string.replace(' ', '_', len(my_string))

    return my_string


def get_links_for_articles(article_type, page):
    url = 'https://www.nature.com/nature/articles'
    params = {'sort': 'PubDate', 'year': '2020', 'page': page}
    headers = {'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'utf-8'}
    url_p = urlparse(url)

    r = requests.get(url, params, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    articles_l = {}
    b = soup.find_all('li', {"class": "app-article-list-row__item"})

    for b1 in b:
        b2 = b1.find('span', {'class': 'c-meta__type'}).text

        if b2 == article_type:
            a = b1.find('a')
            a_link = url_p[0] + '://' + url_p[1] + a['href']
            article = remove_punctuation(a.text.strip())
            articles_l[article + '.txt'] = a_link

    return articles_l


def get_article_content(article_url):
    headers = {'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'utf-8'}

    r = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup.find('div', {'class': 'c-article-body'}).text.strip()


# Getting user input
pages_to_scrap = int(input())  # number to pages to scrap
t_articles = input()  # article name to search

articles = {}
directory = 'Page_'

for n in range(pages_to_scrap):
    articles = get_links_for_articles(t_articles, n + 1)

    if os.path.exists(directory + str(n + 1)) is False:
        os.mkdir(directory + str(n + 1))

    for link in articles:
        os.chdir(directory + str(n + 1))

        with open(link, 'w', encoding='utf-8') as source_file:
            source_file.write(get_article_content(articles[link]))

        os.chdir('..')

    art = ', '.join(articles)

    print(f'Folder: {directory}{str(n + 1)}, Files: {art} \n')
