# Generated by Django 3.0.5 on 2021-04-18 15:30

from django.db import migrations, models
import djongo.models.fields
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaxRating',
            fields=[
                ('_objectid', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('emailid', models.CharField(max_length=50)),
                ('codechef_handle', models.CharField(max_length=50)),
                ('codechef_maxrating', models.IntegerField(default=0)),
                ('codeforces_handle', models.CharField(max_length=50)),
                ('codeforces_maxrating', models.IntegerField(default=0)),
                ('atcoder_handle', models.CharField(max_length=50)),
                ('atcoder_maxrating', models.IntegerField(default=0)),
                ('spoj_handle', models.CharField(max_length=50)),
                ('spoj_maxrating', models.IntegerField(default=0)),
                ('hackerrank_handle', models.CharField(max_length=50)),
                ('hackerrank_maxrating', models.IntegerField(default=0)),
                ('hackerearth_handle', models.CharField(max_length=50)),
                ('hackerearth_maxrating', models.IntegerField(default=0)),
                ('interviewbit_handle', models.CharField(max_length=50)),
                ('interviewbit_maxrating', models.IntegerField(default=0)),
                ('leetcode_handle', models.CharField(max_length=50)),
                ('leetcode_maxrating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('_objectid', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('emailid', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('rollno', models.CharField(max_length=50)),
                ('year_of_pass', models.IntegerField(default=-1)),
                ('course_type', models.CharField(max_length=50)),
                ('codechef_handle', models.CharField(max_length=50)),
                ('codeforces_handle', models.CharField(max_length=50)),
                ('atcoder_handle', models.CharField(max_length=50)),
                ('spoj_handle', models.CharField(max_length=50)),
                ('hackerrank_handle', models.CharField(max_length=50)),
                ('hackerearth_handle', models.CharField(max_length=50)),
                ('interviewbit_handle', models.CharField(max_length=50)),
                ('leetcode_handle', models.CharField(max_length=50)),
                ('github_handle', models.CharField(max_length=50)),
                ('linkedin_handle', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyChange',
            fields=[
                ('_objectid', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('codeforces', jsonfield.fields.JSONField()),
            ],
        ),
    ]
