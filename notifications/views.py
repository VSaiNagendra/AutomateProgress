from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from notifications.models import User, WeeklyChange, MaxRating
from datetime import date,datetime,timedelta
import urllib,json
from urllib.request import urlopen,Request
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
import time
check_status = False


def send_email(request):
	values = {}
	# buildWeeklyUpdate()
	# buildOverallMaxRatings()
	topratingchangeslist, maxratinglist = getRatingUpdatesLastWeek()
	overalltopmaxratings = getOverallMaxRatings()
	startdate, enddate = previous_week_range(date.today())
	startdatestringformat, enddatestringformat = (startdate.strftime("%-d %b %Y"),
		enddate.strftime("%-d %b %Y"))
	values = {
		'startdate': startdatestringformat,
		'enddate': enddatestringformat,
		'weekratingchanges': topratingchangeslist,
		 'weekmaxratings' : maxratinglist,
		 'overalltopmaxratings' : overalltopmaxratings
	}
	subject = 'Rating updates by b&b'
	html_message = render_to_string('notifications/email.html', values)
	plain_message = strip_tags(html_message)
	email_from = settings.EMAIL_HOST_USER
	to = ['sainagendra222@gmail.com', 'saladibalavijayakrishna@gmail.com']
	send_mail( subject, plain_message, email_from,to, html_message=html_message)
	return HttpResponse('Request returned')

def getRatingUpdatesLastWeek():
	weekobjectqueryset = WeeklyChange.objects.filter(enddate=(date.today()+timedelta(days=-1)))
	if(len(weekobjectqueryset)==0):
		return [], []
	weekobject = weekobjectqueryset[0]
	maxratinglist = []
	topratingchangeslist = []
	for username, uservalue in weekobject.codeforces.items():
		topratingchangeslist.append((username,uservalue['ratingChange']))
		maxratinglist.append((username,uservalue['totalMax']))
	topratingchangeslist.sort(key=lambda x:-x[1])
	maxratinglist.sort(key=lambda x:-x[1])
	return topratingchangeslist, maxratinglist

def getOverallMaxRatings():
	overalltopmaxratings = []
	maxratingsqueryset = MaxRating.objects.all()
	for individualmaxrating in maxratingsqueryset:
		overalltopmaxratings.append((individualmaxrating.codeforces_handle,
			individualmaxrating.codeforces_maxrating))
	overalltopmaxratings.sort(key = lambda x:-x[1])
	return overalltopmaxratings[0:min(len(overalltopmaxratings),10)]

def email(request):
	values = {}
	# buildWeeklyUpdate()
	# buildOverallMaxRatings()
	topratingchangeslist, maxratinglist = getRatingUpdatesLastWeek()
	overalltopmaxratings = getOverallMaxRatings()
	startdate, enddate = previous_week_range(date.today())
	startdatestringformat, enddatestringformat = (startdate.strftime("%-d %b %Y"),
		enddate.strftime("%-d %b %Y"))
	print(startdatestringformat,enddatestringformat)
	values = {
		'startdate': startdatestringformat,
		'enddate': enddatestringformat,
		'weekratingchanges': topratingchangeslist,
		 'weekmaxratings' : maxratinglist,
		 'overalltopmaxratings' : overalltopmaxratings
	}
	return render(request,'notifications/email.html',values)

def previous_week_range(date):
    start_date = date + timedelta(days=-7)
    end_date = date + timedelta(days=-1)
    return start_date, end_date
def buildData(request):
	buildWeeklyUpdate()
	buildOverallMaxRatings()
	return HttpResponse('Data build successful.')
def buildWeeklyUpdate():
	codeforces_object = dict()
	start_date,end_date = previous_week_range(date.today())
	start_date = datetime.combine(start_date,datetime.min.time())
	end_date = datetime.combine	(end_date,datetime.max.time())
	user_data = User.objects.all()
	request_count=0
	for user in user_data.iterator():
		req = Request('https://codeforces.com/api/user.rating?handle='+user.codeforces_handle)
		request_count+=1 
		if(request_count==5):
			time.sleep(2)
			request_count = 0
		req.add_header('accept-language','en-US')
		try:
			resp = urlopen(req)
		except urllib.error.HTTPError as err:
			print('Inside Weekly Update')
			print('Error for '+user.codeforces_handle)
			continue
		content = json.loads(resp.read().decode('utf-8'))
		if content['status']!='OK':
			print('Error for status at'+user.codeforces_handle)
			continue
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
		if maxr==None:
			continue
		codeforces_object[user.codeforces_handle]=dict()
		codeforces_object[user.codeforces_handle]['startRating']=minr
		codeforces_object[user.codeforces_handle]['endRating']=maxr
		codeforces_object[user.codeforces_handle]['totalMax']= totalMax
		codeforces_object[user.codeforces_handle]['ratingChange']=maxr-minr
	if(len(codeforces_object.keys())!=0):
		start_date_string = str(start_date.date())
		end_date_string = str(end_date.date())
		week = WeeklyChange(startdate=start_date_string,enddate=end_date_string,codeforces=codeforces_object)
		week.save()
		return (start_date_string, end_date_string)

def buildOverallMaxRatings():
	user_data = User.objects.all()
	request_count = 0
	for user in user_data.iterator():
		req = Request('https://codeforces.com/api/user.rating?handle='+user.codeforces_handle)
		request_count+=1
		if(request_count==5):
			time.sleep(2)
			request_count = 0
		req.add_header('accept-language','en-US')
		try:
			resp = urlopen(req)
		except urllib.error.HTTPError as err:
			print('Error for '+user.codeforces_handle)
			continue
		content = json.loads(resp.read().decode('utf-8'))
		if content['status']!='OK':
			print('Error for status at'+user.codeforces_handle)
			continue
		maxRatingQuerySet = MaxRating.objects.filter(codeforces_handle=user.codeforces_handle);
		print(maxRatingQuerySet)
		maxRating = None
		if(len(maxRatingQuerySet)==0):
			maxRating = MaxRating(codeforces_handle=user.codeforces_handle,codeforces_maxrating=0)
		else:
			maxRating = maxRatingQuerySet[0]
		totalMaxRatingOfUserInAllContests = maxRating.codeforces_maxrating
		for contest in content['result']:
			totalMaxRatingOfUserInAllContests = max(totalMaxRatingOfUserInAllContests,contest['newRating'],contest['oldRating'])
		maxRating.codeforces_maxrating = totalMaxRatingOfUserInAllContests
		maxRating.save()
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
    buildOverallMaxRatings()
    return HttpResponse('Request returned')


