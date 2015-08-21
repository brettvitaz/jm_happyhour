import bottle
import datetime
from dateutil import parser
import requests

URL = 'http://gd2.mlb.com/components/game/mlb/year_{:d}/month_{:02d}/day_{:02d}/master_scoreboard.json'


def get_home_game_for_date(year, month, day):
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

        return result
    except Exception as e:
        print('Something bad happened.', e)


@bottle.post('/happyhour')
@bottle.get('/happyhour')
def get_today():
    data = ''
    date = datetime.datetime.now()
    if bottle.request.method == 'POST':
        try:
            if bottle.request.json:
                query = bottle.request.json['query']
            else:
                query = bottle.request.forms['query']
            date = parser.parse(query)
        except KeyError:
            data = 'Request did not contain a query. Please try again.</p><p>'
        except ValueError:
            data = 'Date was not formatted properly. Please try again.</p><p>'

    form = '''
<p>{{!data}}</p>
<form action="/happyhour" method="post">
    Check another date: <input name="query" type="text" />
    <input value="Submit" type="submit" />
</form>
        '''
    data += get_data(date.year, date.month, date.day)
    return bottle.template(form, data=data)


@bottle.get('/api/happyhour/<year>/<month>/<day>')
def get_data(year=None, month=None, day=None):
    result = get_home_game_for_date(int(year), int(month), int(day))
    if result:
        return 'On {}/{}/{} - Stay home. :('.format(month, day, year)
    return 'On {}/{}/{} - Let\'s get drunk! :D'.format(month, day, year)


bottle.run(host='0.0.0.0', port=8181)
