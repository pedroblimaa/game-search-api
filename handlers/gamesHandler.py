from bs4 import BeautifulSoup
from datetime import date

baseURL = 'https://www.metacritic.com/browse/games/score/metascore/all/pc'


def getGameInfoFromRawHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find(id='main_content')
    generalInfos = results.find_all('td', class_='clamp-summary-wrap')
    images = results.find_all('td', class_='clamp-image-wrap')

    return {
        'generalInfos': generalInfos,
        'images': images
    }


def handleGameInfo(info, image, yearRange=None):
    title = info.find('h3').get_text()
    score = info.find('div', class_='metascore_w').get_text()
    details = info.find('div', class_='clamp-details')
    releaseDate = details.find('span', class_='').get_text()
    releaseYear = releaseDate.split(' ')[-1]
    image = image.find('img')['src']

    if isBetweenYearRange(yearRange, releaseYear):
        return {
            'title': title,
            'score': score,
            'image': image,
            'releaseYear': releaseYear
        }

    return None


def isBetweenYearRange(yearRange, releaseYear):
    if yearRange[0] is None:
        return True

    startYear = yearRange[0]
    endYear = yearRange[1] if yearRange[1] is not None else date.today().year

    return int(startYear) <= int(releaseYear) <= int(endYear)


def getNextPageUrl(URL):
    currentPage = int(URL.split('=')[-1])
    return baseURL + '?page=' + str(currentPage + 1)


def removeGamesBeforeStartGame(games, startGame):
    if startGame is None:
        return games

    for index, game in enumerate(games):
        if game['title'] == startGame:
            return games[index + 1:]

    return games
