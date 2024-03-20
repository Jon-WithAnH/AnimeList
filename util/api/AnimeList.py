import requests
from models.AnimeList.AnimeList import *
from constant.private import *

class AnimeList:
    def __init__(self) -> None:
        self.next = None
        pass

    def getAnimes(self, getNext=False) -> list[AnimeListingClass]:
        headers = {
            'X-MAL-CLIENT-ID': SECRET
        }
        if getNext:
            if self.next is None:
                return None
            url = self.next
        else:
            url = 'https://api.myanimelist.net/v2/users/Tiddilywinkus/animelist?fields=list_status&limit=100'
        ret = requests.get(url, headers=headers)
        response = ret.json() 
        showInfo = response['data']
        self.next = response['paging'].get('next', None)
        listings = []
        for each in showInfo:
            tmp = AnimeListingClass(each)
            listings.append(tmp)
        return listings

    def getManga(self):
        headers = {
            'X-MAL-CLIENT-ID': SECRET
        }
        url = 'https://api.myanimelist.net/v2/users/Tiddilywinkus/mangalist'
        ret = requests.get(url, headers=headers)
        value = ret.json()
        print(value)
        # for each in value:
            # print(each)
