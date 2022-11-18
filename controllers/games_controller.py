import requests as requests
from bs4 import BeautifulSoup

import handlers.games_handler as games_handler

base_URL = 'https://www.metacritic.com/browse/games/score/metascore/all/pc'

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


def get_all(game_list=[], year_range=None, URL=base_URL):
    page = requests.get(URL, headers=headers)
    game_html_info_list = games_handler.get_game_info_from_raw_html(page.content)

    general_infos = game_html_info_list.get('general_infos')
    images = game_html_info_list.get('images')

    game_list = [] if game_list is None else game_list

    for general_info, image in zip(general_infos, images):
        gameInfo = games_handler.handle_game_info(general_info, image, year_range)

        if gameInfo is not None:
            game_list.append(gameInfo)

    return game_list


def get_games_by_year_range(year_range, start_page=0, start_game=None):
    game_list = []
    URL = base_URL + '?page=' + str(start_page)

    while len(game_list) < 100:
        new_game_list = get_all(game_list, year_range, URL)

        new_game_list = games_handler.remove_games_before_start_game(new_game_list, start_game)
        start_game = None

        URL = games_handler.get_next_page_url(URL)
        game_list.extend(new_game_list)

    next_page = games_handler.get_next_page_url(URL).split('=')[-1]

    return {
        'data': game_list[:100],
        'next_page': next_page
    }
