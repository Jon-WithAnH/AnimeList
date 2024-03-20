from util.api.AnimeList import AnimeList
from tinydb import TinyDB, Query

db = TinyDB('./database.json')
t = AnimeList()
table = db.table('EldListings')
s = Query()

listings = t.getAnimes()
for each in listings:
    search = table.search(s['showId'] == each.show.showId)
    if search == []:
        # a new show was added
        table.insert({'showId': each.show.showId, 'title': each.show.title, 'rating': each.rankDetails.score, 'timesChanged': 0, 'oldScores': []})
    else:
        # existing, we'll make sure the scores match
        s2 = table.search((s['showId'] == each.show.showId) & (s['rating'] == each.rankDetails.score))
        if s2 == []:
            # they done. update details
            oldRecord =  table.search(s['showId'] == each.show.showId)[0]
            timesChanged = oldRecord['timesChanged']
            oldScores = oldRecord['oldScores']
            oldScores.append(oldRecord['rating'])
            table.update({'rating': each.rankDetails.score, 'timesChanged': timesChanged+1, 'oldScores': oldScores}, s['showId'] == each.show.showId)