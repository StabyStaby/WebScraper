import requests
from bs4 import BeautifulSoup

def test():
    manganato = 'https://manganato.com/'
    mangadex = 'https://mangatx.com/'
    manga = ["https://manganato.com/manga-mk990067","https://readmanganato.com/manga-nc990759","https://readmanganato.com/manga-mg989415","https://readmanganato.com/manga-ko987549"]
    # manganatoList = getMangaList(u,manganato)
    # mangadexList = getMangaList(u,mangadex)
    htmlTextManganato = requests.get(manganato).text
    htmlTextMangadex = requests.get(mangadex).text
    manganatoSoup = BeautifulSoup(htmlTextManganato,"lxml")
    mangadexSoup = BeautifulSoup(htmlTextMangadex,"lxml")
    allManganato = manganatoSoup.find_all('a',class_ = "tooltip item-img")
    for mange in allManganato:
        if mange['href'] in manga:
            print('aleksa gay')
    # print(manganatoSoup.find_all('a',class_ = 'tooltip item-img')['href'])

test()