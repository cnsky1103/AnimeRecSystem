import json


class Anime:
    def __init__(self, name, tags=[], score=0):
        self.name = name
        self.tags = tags
        self.score = score

    def add_score(self, score):
        self.score = score

    def add_tag(self, tag):
        self.tags.append(tag)


class AnimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Anime):
            return {'name': obj.name, "score": obj.score, "tags": obj.tags}
        elif isinstance(obj, list):
            return [{'name': item.name, "score": item.score, "tags": item.tags} for item in obj]
        else:
            return json.JSONEncoder.default(self, obj)


class AnimeDecoder(json.JSONDecoder):
    def decode(self, s: str):
        result = super().decode(s)
        if isinstance(result, list):
            return [Anime(name=item['name'], tags=item['tags'], score=item['score']) for item in result]
        else:
            return Anime(name=result['name'], tags=result['tags'], score=result['score'])


class Tag:
    def __init__(self, name, animes=[], weight=1):
        self.name = name
        self.animes = animes
        self.weight = weight

    def add_anime(self, anime_name):
        self.animes.append(anime_name)


class TagEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tag):
            return {"name": obj.name, "animes": obj.animes, "weight": obj.weight}
        elif isinstance(obj, list):
            return [{"name": item.name, "animes": item.animes, "weight": item.weight} for item in obj]
        else:
            return json.JSONEncoder.default(self, obj)


class TagDecoder(json.JSONDecoder):
    def decode(self, s):
        result = super().decode(s)
        if isinstance(result, list):
            return [Tag(name=item['name'], animes=item['animes'], weight=item['weight']) for item in result]
        else:
            return Tag(name=result['name'], animes=result['animes'], weight=result['weight'])
