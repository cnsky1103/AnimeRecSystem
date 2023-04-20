from ARS import get_score
from loader import load

animes, tags = load()

t = ["TV", "Doga Kobo", "Manga", "Drama", "Supernatural", "Reincarnation", "Showbiz"]

a = animes['[Oshi No Ko]']
print(a.tags)
print(get_score(a, [tags[item] for item in t]))