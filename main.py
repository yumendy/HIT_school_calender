import datetime
import json

import sys


class CalenderApp(object):
    def __init__(self, first_day='2017-02-27', week_num=18, events=None, beauty=False):
        if events is None:
            events = {}
        self.first_day = datetime.date(*tuple(map(int, first_day.split('-'))))
        self.week_num = week_num
        self.events = events
        self.beauty = beauty

    def get_a_date_obj(self, current_date):
        event = self.events.get(current_date.strftime("%Y-%m-%d"), None)
        if event is not None:
            event = event.encode('utf8')
        return {
            "date": current_date.strftime("%Y-%m-%d"),
            "weekday": current_date.isoweekday(),
            "events": event
        }

    def gen_json(self):
        weeks_list = []
        current_date = self.first_day
        for week_no in xrange(1, self.week_num + 1):
            week = {'week_number': week_no, 'dates': []}
            for i in xrange(7):
                week['dates'].append(self.get_a_date_obj(current_date))
                current_date += datetime.timedelta(days=1)
            weeks_list.append(week)
        return json.dumps({'weeks': weeks_list}, indent=4 if self.beauty else None, encoding='utf8')


if __name__ == '__main__':
    arg_dict = None
    with open(sys.argv[1], 'rb') as fp:
        arg_dict = json.load(fp, encoding='utf8')
    app = CalenderApp(**arg_dict)
    with open('output.json', 'wb') as fp:
        fp.write(app.gen_json())
