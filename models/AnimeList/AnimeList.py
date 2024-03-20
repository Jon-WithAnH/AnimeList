class AnimeShow:
    def __init__(self, data: dict) -> None:
        self.showId = data['id']
        self.title = data['title']
        self.largeImage = data['main_picture']['large']
        self.mediumImage = data['main_picture']['medium']

class AnimeShowRanking:
    def __init__(self, data: dict) -> None:
        self.status = data['status']
        self.score = data['score']
        self.num_episodes_watched = data['num_episodes_watched']
        self.is_rewatching = data['is_rewatching']
        self.updated_at = data['updated_at']

class AnimeListingClass:
    def __init__(self, data: dict) -> None:
        self.show = AnimeShow(data['node'])
        self.rankDetails = AnimeShowRanking(data['list_status'])