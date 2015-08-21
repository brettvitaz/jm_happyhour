import bottle
import datetime
from dateutil import parser

from jm_happyhour import get_daily_schedule


@bottle.post('/happyhour')
@bottle.get('/happyhour')
def get_today():
    date = datetime.datetime.now()
    if bottle.request.method == 'POST':
        try:
            if bottle.request.json:
                query = bottle.request.json['query']
            else:
                query = bottle.request.forms['query']
            date = parser.parse(query)
        except KeyError:
            bottle.abort(500, 'Request did not contain a query.')
    form = '''
<p>{{data}}</p>
<form action="/happyhour" method="post">
    Check another date: <input name="query" type="text" />
    <input value="Submit" type="submit" />
</form>
        '''
    data = get_data(date.year, date.month, date.day)
    return bottle.template(form, data=data)

@bottle.get('/api/happyhour/<year>/<month>/<day>')
def get_data(year=None, month=None, day=None):
    result = get_daily_schedule.get_master_scoreboard(int(year), int(month), int(day))
    if result:
        return 'On {}/{}/{} - Stay home. :('.format(month, day, year)
    return 'On {}/{}/{} - Let\'s get drunk! :D'.format(month, day, year)

@bottle.get('/api/happyhour')
@bottle.post('/api/happyhour')
def handle_query():
    try:
        if bottle.request.json:
            query = bottle.request.json['query']
        else:
            query = bottle.request.forms['query']
        date = parser.parse(query)
        return get_data(date.year, date.month, date.day)
    except KeyError:
        bottle.abort(500, 'Request did not contain a query.')

bottle.run(host='0.0.0.0', port=8181)
