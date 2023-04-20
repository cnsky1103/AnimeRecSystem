import json
from model import AnimeDecoder, TagDecoder

def load():
    with open('./data/animes.json', 'r') as f:
        json_string = f.read()
        animes = json.loads(json_string, cls=AnimeDecoder)
    with open('./data/tags.json', 'r') as f:
        json_string = f.read()
        tags = json.loads(json_string, cls=TagDecoder)
        
    animes_dict = {}
    tags_dict = {}
    for a in animes:
        animes_dict[a.name] = a
    for t in tags:
        tags_dict[t.name] = t
    return animes_dict, tags_dict