class Sql_AnimeShowRanking:
    def __init__(self, data: dict|list) -> None:
        # coming from mysql
        self.rankId = data[5]
        self.status = data[0]
        self.score = data[1]
        self.num_episodes_watched = data[2]
        self.is_rewatching = data[3]
        self.updated_at = data[4]