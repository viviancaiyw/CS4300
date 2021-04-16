"""This file crawl data from Steam API"""
import json
import os
from typing import Dict, List

import requests

CUR_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(CUR_FOLDER, 'web_crawl_data')
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
APP_ID_LIST = os.path.join(DATA_FOLDER, 'app_ids.json')
APP_DETAILS_DIR = os.path.join(DATA_FOLDER, 'app_details')


def download_all_game_ids(outfile: str = APP_ID_LIST) -> Dict[str, List[int]]:
    """
    Download all existing games ids from Steam API, write to outfile
    :param outfile: the output file
    :return: dict format of the json written to the outfile
    """
    link = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    params = {
        'language': 'english',
        'format': 'json'
    }
    response = requests.get(url=link, params=params)
    data = response.json()
    json.dump({'app_ids': _get_app_ids(data)}, open(outfile, 'w+'))
    return data


def _get_app_ids(app_dict: Dict[str, Dict]):
    """
    Helper methods to remove name field from json, keeping only app ids
    """
    app_list = app_dict['applist']['apps']
    print(f"number of apps: {len(app_list)}")
    ids = list()
    for app_info in app_list:
        ids.append(app_info['appid'])
    return ids


def get_game_details():
    """
    Downloads all games details
    """
    pass


if __name__ == '__main__':
    download_all_game_ids()
