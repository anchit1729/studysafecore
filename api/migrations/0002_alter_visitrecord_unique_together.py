# Generated by Django 4.0.3 on 2022-04-15 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='visitrecord',
            unique_together={('member_uid', 'venue_code', 'access_type', 'record_datetime')},
        ),
    ]
