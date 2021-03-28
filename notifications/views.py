from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from notifications.models import User

def start_view(request):
	u=User()
	u.emailid='someemailid'
	u.codeforces_handle='vsainagendra'
	u.username='temporary'
	u.save()
	return HttpResponse('Page found')
