import datetime
import requests

URL = 'http://gd2.mlb.com/components/game/mlb/year_{:d}/month_{:02d}/day_{:02d}/master_scoreboard.json'


def get_master_scoreboard(year, month, day):
    try:
        info = requests.get(URL.format(year, month, day))

        result = False

        if 'data' in info.json():
            if 'games' in info.json()['data']:
                games = info.json()['data']['games']['game']
                if isinstance(games, dict):
                    games = [games]
                for game in games:
                    if game['location'].startswith('Seattle'):
                        result = True
                        break

        # print(year, month, day, info.json().get('data', {}).get('games', {}).get('game', {}))
        print(year, month, day, result)
        return result
    except Exception as e:
        print(year, month, day, e)

    # print([game['location'] for game in info.json()['data']['games']['game']])


if __name__ == '__main__':
    start_date = datetime.date(2015, 1, 1)
    day_count = 0
    while day_count < 365:
        day_lookup = start_date + datetime.timedelta(days=day_count)
        get_master_scoreboard(day_lookup.year, day_lookup.month, day_lookup.day)
        day_count += 1
