import requests
from bs4 import BeautifulSoup
import re
import json


class Anime:
    def __init__(self, name) -> None:
        self.name = name
        self.tags = []

    def add_score(self, score):
        self.score = score

    def add_tag(self, tag):
        self.tags.append(tag)


class AnimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Anime):
            return {'name': obj.name, "score": obj.score, "tags": obj.tags}
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        else:
            return json.JSONEncoder.default(self, obj)


class Tag:
    def __init__(self, name) -> None:
        self.name = name
        self.animes = []

    def add_anime(self, anime_name):
        self.animes.append(anime_name)


class TagEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tag):
            return {"name": obj.name, "animes": obj.animes}
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        else:
            return json.JSONEncoder.default(self, obj)


animes = {}
tags = {}


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getAnimeList(html):
    soup = BeautifulSoup(html, "html.parser")
    hrefList = soup.find_all(
        'a', attrs={'class': 'hoverinfo_trigger fl-l ml12 mr8'})
    for href in hrefList:
        url = href.attrs['href']
        extractAnimeInfo(url)


def extractTextFromLabel(label):
    if isinstance(label, str):
        return label.strip()
    else:
        return label.text.strip()


def extractTag(label):
    return extractTextFromLabel(label.nextSibling)


def extractAnimeInfo(url):
    try:
        soup = BeautifulSoup(getHTMLText(url), "html.parser")
        score = soup.find('span', attrs={
            'itemprop': 'ratingValue', 'class': re.compile('score-label score-')})
        spans = soup.find_all('span', attrs={'class': 'dark_text'})
        anime = None
        title = soup.find('p', attrs={'class': 'title-english title-inherit'})
        if title is not None:
            anime = Anime(title.text.strip())
        else:
            title = soup.find('h1', attrs={'class': 'title-name h1_bold_none'})
            anime = Anime(title.findChild('strong').text.strip())
        anime.add_score(float(score.text.strip()))
        # single_tag_list = ['Type:', "Source:"]
        # multi_tag_list = ["Studios:", "Genres:", "Themes:"]
        t = []
        for span in spans:
            if span.text == 'Type:':
                if span.next_sibling.next_sibling is not None:
                    t.append(span.next_sibling.next_sibling.text.strip())
                else:
                    t.append(span.next_sibling.text.strip())
            elif span.text == 'Source:':
                t.append(span.next_sibling.text.strip())
            elif span.text == 'Studios:':
                t.append(span.next_sibling.next_sibling.text.strip())
            elif span.text == 'Genres:':
                next = span.next_sibling
                while next is not None:
                    if next.name == 'a':
                        t.append(next.text.strip())
                    next = next.next_sibling
            elif span.text == 'Themes:':
                next = span.next_sibling
                while next is not None:
                    if next.name == 'a':
                        t.append(next.text.strip())
                    next = next.next_sibling
        for tag in t:
            if tag not in tags:
                tags[tag] = []
            tags[tag].append(anime.name)
            anime.add_tag(tag)
        animes[anime.name] = anime
    except Exception as e:
        print(e)


if __name__ == "__main__":
    pages = 10
    for i in range(pages):
        url = f"https://myanimelist.net/topanime.php?limit={i*50}"
        html = getHTMLText(url)
        getAnimeList(html)

    with open('data/animes.json', 'w') as file:
        json.dump(animes, file, cls=AnimeEncoder)

    with open('data/tags.json', 'w') as file:
        json.dump(tags, file, cls=TagEncoder)
