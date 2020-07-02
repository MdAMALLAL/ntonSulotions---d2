from django.core.management.base import BaseCommand, CommandError
import os
from crontab import CronTab

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #init cron
        cron = CronTab()

        #add new cron job
        job = cron.new(command='python3 manage.py report_uncharged_emails >>/tmp/out.txt 2>&1')

        #job settings
        job.hour.every(8)

        cron.write()
