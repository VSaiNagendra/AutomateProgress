from djongo import models
from jsonfield import JSONField
class User(models.Model):
	_objectid = models.ObjectIdField()
	emailid = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	rollno = models.CharField(max_length=50)
	year_of_pass = models.IntegerField(default=-1)
	course_type = models.CharField(max_length=50)
	codechef_handle = models.CharField(max_length=50)
	codeforces_handle = models.CharField(max_length=50)
	atcoder_handle = models.CharField(max_length=50)
	spoj_handle = models.CharField(max_length=50)
	hackerrank_handle = models.CharField(max_length=50)
	hackerearth_handle = models.CharField(max_length=50)
	interviewbit_handle = models.CharField(max_length=50)
	leetcode_handle = models.CharField(max_length=50)
	github_handle = models.CharField(max_length=50)
	linkedin_handle = models.CharField(max_length=50)

class WeeklyChange(models.Model):
	_objectid = models.ObjectIdField() 
	startdate = models.DateField()
	enddate = models.DateField()
	codeforces = JSONField()
