import requests as requests
from bs4 import BeautifulSoup

import handlers.gamesHandler as gamesHandler

baseURL = 'https://www.metacritic.com/browse/games/score/metascore/all/pc'

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                  'Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


def getAll(gameList=[], yearRange=None, URL=baseURL):
    page = requests.get(URL, headers=headers)
    gameHtmlInfoList = gamesHandler.getGameInfoFromRawHtml(page.content)

    generalInfos = gameHtmlInfoList.get('generalInfos')
    images = gameHtmlInfoList.get('images')

    gameList = [] if gameList is None else gameList

    for generalInfo, image in zip(generalInfos, images):
        gameInfo = gamesHandler.handleGameInfo(generalInfo, image, yearRange)

        if gameInfo is not None:
            gameList.append(gameInfo)

    return gameList


def getGamesByYearRange(yearRange, startPage=0, startGame=None):
    gameList = []
    URL = baseURL + '?page=' + str(startPage)

    while len(gameList) < 100:
        newGameList = getAll(gameList, yearRange, URL)

        newGameList = gamesHandler.removeGamesBeforeStartGame(newGameList, startGame)
        startGame = None

        URL = gamesHandler.getNextPageUrl(URL)
        gameList.extend(newGameList)

    nextPage = gamesHandler.getNextPageUrl(URL).split('=')[-1]

    return {
        'data': gameList[:100],
        'nextPage': nextPage
    }
