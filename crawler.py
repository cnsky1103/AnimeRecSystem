import requests
from bs4 import BeautifulSoup
import re
import json
from model import Anime, AnimeEncoder, Tag, TagEncoder

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
                    t.append((span.next_sibling.next_sibling.text.strip(), 0.3))
                else:
                    t.append((span.next_sibling.text.strip(), 0.3))
            elif span.text == 'Source:':
                t.append((span.next_sibling.text.strip(), 0.5))
            elif span.text == 'Studios:':
                t.append((span.next_sibling.next_sibling.text.strip(), 0.3))
            elif span.text == 'Genres:':
                next = span.next_sibling
                while next is not None:
                    if next.name == 'a':
                        t.append((next.text.strip(), 1))
                    next = next.next_sibling
            elif span.text == 'Themes:':
                next = span.next_sibling
                while next is not None:
                    if next.name == 'a':
                        t.append((next.text.strip(), 1))
                    next = next.next_sibling
        for tag in t:
            if tag[0] not in tags:
                tags[tag[0]] = Tag(name=tag[0], animes=[], weight=tag[1])
            tags[tag[0]].animes.append(anime.name)
            anime.add_tag(tag[0])
        animes[anime.name] = anime
    except Exception as e:
        pass


if __name__ == "__main__":
    pages = 5
    for i in range(pages):
        url = f"https://myanimelist.net/topanime.php?limit={i*50}"
        html = getHTMLText(url)
        getAnimeList(html)

    with open('data/animes.json', 'w') as file:
        json.dump(list(animes.values()), file, cls=AnimeEncoder)

    with open('data/tags.json', 'w') as file:
        json.dump(list(tags.values()), file, cls=TagEncoder)
