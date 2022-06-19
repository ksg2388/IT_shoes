# import calendar
# c = calendar.TextCalendar(calendar.SUNDAY)
# for i in range(12):
#     s = c.formatmonth(2022,i+1)
#     print(s)

from flask import Flask , g, request, Response, make_resopnse
from flask import session, render_template, markup, url_for
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

app = Flask(__name__)
app.debug = True

app.config.update(
    SECRET_KEY = '123456789',
    SESSION_COOKIE_NAME = 'pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME = timedelta(31)
)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

class FormInput:
    def __init__(self, id= '', name ='', value ='', checked = '', text ='', type ='text'):
        self.id = id
        self.name = name
        self.value = value
        self.chekced = checked
        self.text = text
        self.type = type
        

@app.template_filter('ymd')
def datetime_ymd(dt, fmt = '%m - %d'):
    if isinstance(dt,date):
        return "<strong>%s</strong>" %dt.strftime(fmt)
    else:
        return dt
    
@app.template_filter('simpledate')
def simpledate(dt):
    if not isinstance(dt, date):
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        
    if(datetime.now() - dt).days < 1:
        fmt = '%H:%M'
    else:
        fmt = "%m/%d"
        
    return "<strong>%s</strong>" %dt.strftime(fmt)

def make_date(dt, fmt):
    if not isinstance(dt, date):
        return datetime.strptime(dt, fmt)
    else:
        return dt

@app.template_filter('sdt')
def sdt(dt,fmt):
    d = make_date(dt, fmt)
    wd = d.weekday()
    return -1 if wd == 6 else wd * -1

@app.template_filter('month')
def month(dt, fmt ='%Y-%m-%d'):
    d = make_date(dt, fmt)
    return d.month

@app.template_filter('edt')
def edt(dt, fmt = '%Y-%m-%d'):
    d = make_date(dt, fmt)
    nextMonth = d + relativedelta(months = 1)
    edt = (nextMonth - timedelta(1)).day + 1
    return edt
    
    

@app.rout('/')
def idx():
    rds = []
    for i in [1,2,3]:
        id = 'r' + str(i)
        name ='radiotest'
        value = i
        checked = ''
        if i == 2:
            checked = 'checked'
        text = 'Radiotest' + str(i)
        rds.append(FormInput(id,name, value, checked, text))
        
    today = date.today()
    d = datetime.strptime()
    
    sdt = d.weekday() * -1
    nextMonth = d + relativedelta(months = 1)
    mm = d.month
    edt = (nextMonth - timedelta(1)).day + 1
    
    year = 2022
    return render_template('달력.html',year = year, sdt = sdt, edt = edt, mm = mm, ttt = 'test', radioList = rds, today = today )
