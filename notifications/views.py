from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from notifications.models import User, WeeklyChange
from datetime import date
import datetime
import urllib,json
from urllib.request import urlopen,Request

check_status = False

def previous_week_range(date):
    start_date = date + datetime.timedelta(-date.weekday(), weeks=-1)
    end_date = date + datetime.timedelta(-date.weekday() - 1)
    return start_date, end_date

def buildWeeklyUpdate():
    week = WeeklyChange()

    start_date,end_date = previous_week_range(date.today())
    user_data = User.objects.all()
    for user in user_data.iterator():
        req = Request('https://codeforces.com/api/user.rating?handle='+user.codeforces_handle)
        req.add_header('accept-language','en-US')
        try:
            resp = urlopen(req)
        except urllib.error.HTTPError as err:
            print('Error for '+user.codeforces_handle)
            continue
        content = json.loads(resp.read().decode('utf-8'))
        print('content is')
        print(content)


def start_view(request):
	u=User()
	u.emailid='someemailid'
	u.codeforces_handle='vsainagendra'
	u.username='temporary'
	u.save()
	return HttpResponse('Page found')


def run_view(request):
    global check_status
    if check_status:
        return HttpResponse('Automation request is already in progress')
    check_status = True
    buildWeeklyUpdate()
    return HttpResponse('Request returned')


