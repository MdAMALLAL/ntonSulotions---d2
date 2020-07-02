from django.core.management.base import BaseCommand, CommandError
import os
from crontab import CronTab

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #init cron
        cron = CronTab(user='ntonadvisory')

        #add new cron job
        job = cron.new(command='python3 /home/ntonadvisory/public_html/helpdesk/manage.py report_uncharged_emails >>/tmp/out.txt 2>&1')

        #job settings
        job.hour.every(8)

        cron.write()
#*/10 * * * * python3 /home/ntonadvisory/public_html/helpdesk/manage.py report_uncharged_emails >>/tmp/out.txt 2>&1
#0 */8 * * * python3 /home/ntonadvisory/public_html/helpdesk/manage.py report_uncharged_emails >>/tmp/out.txt 2>&1
