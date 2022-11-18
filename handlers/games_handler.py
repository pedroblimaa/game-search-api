from bs4 import BeautifulSoup
from datetime import date

baseURL = 'https://www.metacritic.com/browse/games/score/metascore/all/pc'


def get_game_info_from_raw_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find(id='main_content')
    general_infos = results.find_all('td', class_='clamp-summary-wrap')
    images = results.find_all('td', class_='clamp-image-wrap')

    return {
        'general_infos': general_infos,
        'images': images
    }


def handle_game_info(info, image, year_range=None):
    title = info.find('h3').get_text()
    score = info.find('div', class_='metascore_w').get_text()
    details = info.find('div', class_='clamp-details')
    release_date = details.find('span', class_='').get_text()
    release_year = release_date.split(' ')[-1]
    image = image.find('img')['src']

    if is_between_year_range(year_range, release_year):
        return {
            'title': title,
            'score': score,
            'image': image,
            'release_year': release_year
        }

    return None


def is_between_year_range(year_range, release_year):
    if year_range is None or year_range[0] is None:
        return True

    startYear = year_range[0]
    endYear = year_range[1] if year_range[1] is not None else date.today().year

    return int(startYear) <= int(release_year) <= int(endYear)


def get_next_page_url(URL):
    currentPage = int(URL.split('=')[-1])
    return baseURL + '?page=' + str(currentPage + 1)


def remove_games_before_start_game(games, start_game):
    if start_game is None:
        return games

    for index, game in enumerate(games):
        if game['title'] == start_game:
            return games[index + 1:]

    return games
