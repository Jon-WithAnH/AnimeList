import pyodbc
from constant.private import private
from models.Sql.Users import User
from models.Sql.Show import Show
from models.Sql.AnimeList import *
from models.AnimeList.AnimeList import *

class MySqlConnector:
    def __init__(self) -> None:
        self.curser = None
        self.conn = None
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.curser.close()
        self.conn.close()
    def __enter__(self):
        self.conn = pyodbc.connect(f"DSN=MySql;Uid={private.SQL_USER};Pwd={private.SQL_PASS}")
        self.curser = self.conn.cursor()
        return self
    def commit(self):
        self.conn.commit()
    def getLastInsertedId(self, c: pyodbc.Cursor):
        return c.execute('SELECT LAST_INSERT_ID();').fetchone()[0]

    def getUsers(self):
        self.curser.execute('select * from AnimeWatchList_Users')
        r =  self.curser.fetchall()
        if r == []:
            return None
        return [User(each) for each in r]
    def getUsersByUserName(self, username: str):
        self.curser.execute(f'select * from AnimeWatchList_Users where username = "{username}"')
        r =  self.curser.fetchone()
        if r is None:
            return None
        return User(r)
    
    def InsertUser(self, name: str, commit=True):
        # I hate this. Sql server does it better.
        c = self.curser.execute(f"insert into AnimeWatchList_Users (UserName) values ('{name}');")
        c = c.execute('SELECT LAST_INSERT_ID();')
        r = c.fetchone()[0]
        if commit:
            self.conn.commit()
        return r
    
    def insertNewShow(self, data: AnimeShow):
        query = f"insert into AnimeWatchList_Shows "\
                "(ShowId, Title, MediumImage, LargeImage) "\
                "values "\
                f"({data.showId}, '{data.title}', '{data.mediumImage}', '{data.largeImage}'); "
        c = self.curser.execute(query)
        r = self.getLastInsertedId(c)

        self.commit()
        self.curser.execute(f"select showId from AnimeWatchList_Shows where RecordId={r}")
        return self.curser.fetchone()[0]
    def insertRankChange(self, userId: int, rankId: int, oldRank: int, newRank: int):
        # since this is only an audit record, I'm not going to return anything
        self.curser.execute(f"insert into AnimeWatchList_RankingChanges (UserId,RankingId,OldScore,NewScore) values ({userId},{rankId},{oldRank},{newRank})")
        self.commit()

    def insertFirstShowScore(self, showId, userId, rank: AnimeShowRanking):
        query = "insert into animewatchlist_showrankings (ShowId, UserId, Status, Score, NumberEpisodesWatched, IsRewatching, UpdatedAt) values "\
                f"({showId}, {userId}, '{rank.status}', {rank.score}, {rank.num_episodes_watched}, '{rank.is_rewatching}', '{rank.updated_at}')"
        self.curser.execute(query)
        self.commit()

    def updateRankByRankingId(self, rankingId: int, newScore: int):
        self.curser.execute(f"update AnimeWatchList_ShowRankings set Score={newScore} where RankingId={rankingId}")
        self.commit()
    def getShowByShowId(self, showId: int):
        self.curser.execute(f"select * from AnimeWatchList_Shows where showId = {showId}")
        r = self.curser.fetchone()
        if r is None:
            return None
        return Show(r)
    def getRankingByShowAndUser(self, showId: int, userId: int):
        self.curser.execute(f"select Status,Score,NumberEpisodesWatched, IsRewatching,UpdatedAt,RankingId "\
                            f"from AnimeWatchList_ShowRankings where showId = {showId} and userId = {userId}")
        return Sql_AnimeShowRanking(self.curser.fetchone())
        
