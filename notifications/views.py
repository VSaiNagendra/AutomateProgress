from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from notifications.models import User, WeeklyChange
from datetime import date,datetime,timedelta
import urllib,json
from urllib.request import urlopen,Request

check_status = False

def previous_week_range(date):
    start_date = date + timedelta(-date.weekday(), weeks=-1)
    end_date = date + timedelta(-date.weekday() - 1)
    return start_date, end_date

def buildWeeklyUpdate():
	start_date,end_date = previous_week_range(date.today())
	start_date = datetime.combine(start_date,datetime.min.time())
	end_date = datetime.combine	(end_date,datetime.max.time())
	user_data = User.objects.all()
	for user in user_data.iterator():
		print('Iam here')
		req = Request('https://codeforces.com/api/user.rating?handle='+user.codeforces_handle)
		req.add_header('accept-language','en-US')
		try:
			resp = urlopen(req)
			print('I am there')
			print(resp)
		except urllib.error.HTTPError as err:
			print('Error for '+user.codeforces_handle)
			continue
	content = json.loads(resp.read().decode('utf-8'))
	if content['status']!='OK':
		print('Error for '+user.codeforces_handle)
		return
	print(content)
	minr,maxr=None,None
	totalMax = 0
	for contest in content['result']:
		if start_date<= datetime.fromtimestamp(int(contest['ratingUpdateTimeSeconds'])) and datetime.fromtimestamp(int(contest['ratingUpdateTimeSeconds']))  <= end_date:
			if minr==None:
				minr = contest['oldRating']
				maxr= contest['newRating']
			else:
				maxr= contest['newRating']
			totalMax = max(totalMax,contest['newRating'])
	print(maxr)
	if maxr==None:
		return
	print('I am at week')

	start_date = str(start_date.date())
	end_date = str(end_date.date())
	codeforces_handle = dict()
	codeforces_handle['startRating']=minr
	codeforces_handle['endRating']=maxr
	codeforces_handle['totalMax']= totalMax
	codeforces_handle['ratingChange']=maxr-minr
	week = WeeklyChange(startdate=start_date,enddate=end_date,codeforces=codeforces_handle)
	week.save()



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


