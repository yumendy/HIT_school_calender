import json

import datetime
import web


class Redirect(object):
    def GET(self, path):
        web.seeother('/' + path)


class Event(object):
    def __init__(self, date, event):
        self.date = datetime.date(*tuple(map(int, date.split('-'))))
        self.event = event


class APIServer(object):
    def __init__(self):
        self.event_list = []
        with open('input.json') as fp:
            temp = json.load(fp)
            self.event_list = [Event(date, event) for date, event in temp['events'].iteritems()]

    def __query_event(self, start, end):
        start = datetime.date(*tuple(map(int, [start[:4], start[4:6], start[6:]])))
        end = datetime.date(*tuple(map(int, [end[:4], end[4:6], end[6:]])))
        return filter(lambda event: start <= event.date <= end, self.event_list)

    def __gen_json(self, event_list):
        result = {
            'errcode': 0,
            'errmsg': 'ok',
            'events': []
        }
        for event in event_list:
            ev = {
                'eventid': abs(hash(event.date.strftime("%Y-%m-%d"))),
                'title': event.event,
                'description': event.event,
                'start': event.date.strftime("%Y-%m-%d %H:%M"),
                'end': (event.date + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                'address': '',
                'url': ''
            }
            result['events'].append(ev)
        return json.dumps(result, indent=4)

    def query(self, start, end):
        return self.__gen_json(self.__query_event(start, end))

    def GET(self):
        return self.query(web.input()['start'], web.input()['end'])


if __name__ == '__main__':
    url = (
        '/(.*)/', 'Redirect',
        '/', 'APIServer'
    )
    app = web.application(url, globals())
    app.run()
