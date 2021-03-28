# Generated by Django 3.0.5 on 2021-03-28 14:32

from django.db import migrations, models
import djongo.models.fields
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
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