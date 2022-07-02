from datetime import  datetime, timedelta
from bs4 import BeautifulSoup
from numpy import tile
import requests
from sqlalchemy import Date
from .models import Manga, User



def scrapeForChapters(url):
    print("Call")
    if 'manganato' in url :
        htmlText = requests.get(url).text
        soup = BeautifulSoup(htmlText,'lxml')
        title = soup.find('div',class_='story-info-right')
        print(title.h1.text)
        chapters = soup.find_all('li',class_='a-h')
        for chapter in chapters :
            number = tuple(chapter.find_all('span'))
            date = number[1]['title']+':00'
            data = datetime.strptime(date,"%b %d,%Y %X")    
    return data,len(chapters)

def scrapeForChapter(url):
    # print("Call")
    htmlText = requests.get(url).text
    soup = BeautifulSoup(htmlText,'lxml') 
    if 'manganato' in url :
        title = soup.find('div',class_='story-info-right')
        # print(title.h1.text)
        chapters = soup.find_all('li',class_='a-h')
        chapter = soup.find('li',class_='a-h')
        link = chapter.find('a')['href']
        number = tuple(chapter.find_all('span'))
        date = number[1]['title']+':00'
        data = datetime.strptime(date,"%b %d,%Y %X") 
        return data,str(len(chapters)),link

    if 'mangatx' in url:
        title = soup.find('div',class_='post-title')
        chapters = soup.find_all('li',class_='wp-manga-chapter')
        chapter = soup.find('li',class_='wp-manga-chapter')
        newTag = chapter.find('span',class_='c-new-tag')
        if   newTag :
            date = newTag.a['title']
            if 'days' in date :
                for s in date.split():
                    if s.isdigit():
                        time = int(s)
                data = datetime.now()-timedelta(days=time)
            elif 'hours' in date :
                for s in date.split():
                    if s.isdigit():
                        time = int(s)
                data = datetime.now()-timedelta(hours=time)
            elif 'mins' in date :
                for s in date.split():
                    if s.isdigit():
                        time = int(s)
                data = datetime.now()-timedelta(minutes=time)
            else:
                data = datetime.strptime(date,"%B %d, %Y")
            link = chapter.a['href'] 
        else:
            link = chapter.a['href']
            date = chapter.find('span')
            data = datetime.strptime(date.i.text,"%B %d, %Y")
        print(f"{data}")
        return data,str(len(chapters)),link


def scrapeName(url):
    htmlText = requests.get(url).text
    soup = BeautifulSoup(htmlText,'lxml')
    if 'manganato' in url :
        title = soup.find('div',class_='story-info-right')
    if 'mangatx' in url :
        title = soup.find('div',class_='post-title')
    return title.h1.text

def scrapeForLastDate(url):
    if 'manganato' in url :
        htmlText = requests.get(url).text
        soup = BeautifulSoup(htmlText,'lxml')
        chapters = soup.find('li',class_='a-h')
        number = tuple(chapters.find_all('span'))
        date = number[1]['title']+':00'
        data = datetime.strptime(date,"%b %d,%Y %X")
    return data

# print(scrapeForChapter('https://mangatx.com/manga/escort-warrior/'))

def scrapeManga(url):
    htmlText = requests.get(url).text
    soup = BeautifulSoup(htmlText,'lxml')
    if 'manganato' in url :
        title = soup.find('div',class_='story-info-right')
        titleF = title.h1.text
        chapter = soup.find('li',class_='a-h')
        number = tuple(chapter.find_all('span'))
        date = number[1]['title']+':00'
        data = datetime.strptime(date,"%b %d,%Y %X")
        chapters = soup.find_all('li',class_='a-h')
        img = soup.find('div',class_='story-info-left')
        imgUrl = img.find('img')['src']
    if 'mangatx' in url :
        title = soup.find('div',class_='post-title')
        titleF =''
        for t in title.h1.text.split():
            if 'HOT' not in t:
                titleF+=t
                titleF+=' '
        chapters = soup.find_all('li',class_='wp-manga-chapter')
        chapter = soup.find('li',class_='wp-manga-chapter')
        imgSrc = soup.find('div',class_="summary_image")
        imgUrl = imgSrc.find('img')['data-srcset']
        newTag = chapter.find('span',class_="c-new-tag")
        if   newTag :
            date = newTag.a['title']
            if 'days' in date :
                for s in date.split():
                    if s.isdigit():
                        time = int(s)
                data = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)-timedelta(hours=time)
            elif 'hours' in date :
                for s in date.split():
                    if s.isdigit():
                        time = int(s)
                data = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)-timedelta(hours=time)
            elif 'mins' in date :
                for s in date.split():
                    if s.isdigit():
                        time = int(s)
                data = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)-timedelta(hours=time)
            else:
                data = datetime.strptime(date,"%b %d,%Y %X")
        else:
            date = chapter.find('span')
            data = datetime.strptime(date.i.text,"%B %d, %Y")
    manga = Manga(lastChapterDate=data,name=titleF,url=url,nrOfChapters=len(chapters),imgUrl=imgUrl.split()[0])
    print(f"\n{manga.imgUrl} \n {manga.lastChapterDate} \n {manga.name} \n {manga.nrOfChapters} \n {manga.url}\n")
    return manga

def scrapeHome(u):
    manganato = 'https://manganato.com/'
    mangadex = 'https://mangatx.com/'
    manganatoList = getMangaList(u,manganato)
    mangadexList = getMangaList(u,mangadex)
    htmlTextManganato = requests.get(manganato).text
    htmlTextMangadex = requests.get(mangadex).text
    manganatoSoup = BeautifulSoup(htmlTextManganato,"lxml")
    mangadexSoup = BeautifulSoup(htmlTextMangadex,"lxml")
    allManganato = manganatoSoup.find_all('a',class_ = 'tooltip item-img')
    for manga in allManganato:
        if manga['href'] in manganatoList:
            scrapeManga(manga['href'])
        
        
        
def getMangaList(user,site):
    mangaList = []
    for manga in user.manga:
        if site in manga.url:
            mangaList.append(manga.url)
    return mangaList