from util.api.AnimeList import AnimeList
from util.api.MySql import MySqlConnector
### This will only work for one person because I don't care enough to allow for dynamic naming for the db ###
t = AnimeList()
UsersICareAbout = ['Tiddilywinkus']

listings = t.getAnimes(UsersICareAbout[0])
runtimeChanges = 0
newShows = 0
with MySqlConnector() as sql:
    for DoThisUser in UsersICareAbout:
        listings = t.getAnimes(DoThisUser)
        user = sql.getUsersByUserName(DoThisUser)
        if user is None:
            uid = sql.InsertUser(DoThisUser)
        else:
            uid = user.id
        for each in listings:
            searchResult = sql.getShowByShowId(each.show.showId)
            if searchResult is None:
                showId = sql.insertNewShow(each.show)
                sql.insertFirstShowScore(showId, uid, each.rankDetails)
                newShows += 1
                # a new show was added
            else:
                # existing, we'll make sure the scores match
                s3 = sql.getRankingByShowAndUser(searchResult.ShowId, uid)
                if s3.score != each.rankDetails.score:
                    # they don't. update details
                    sql.insertRankChange(uid, s3.rankId, s3.rankId, each.rankDetails.score)
                    sql.updateRankByRankingId(s3.rankId, each.rankDetails.score)
                    runtimeChanges += 1
print(f"New Shows: {newShows}")
print(f"Total changes: {runtimeChanges}")