import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from datetime import timedelta

from solutions.models import Question
import datetime, pytz
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger()

class Command(BaseCommand):

    commands = ['sendreport',]
    args = '[command]'
    help = 'Send report'

    def handle(self, *args, **options):

        '''
        Get completed sessions, send invite to vote
        '''
        uncharged_questions = Question.objects.filter(created_at__gte=(timezone.now()-timedelta(minute=3)), charged_by__isnull=True)

        for question in uncharged_questions:
            plaintext = get_template('email/email.txt')
            htmly     = get_template('email/email.html')
            subject = _('Ticket not yet taken into account')
            d = {}
            d['ref'] = question.get_ref
            d['object '] = question.objet
            d['user'] = question.user.username
            d['ticket_url'] = "http://{0}{1}".format(self.request.META['HTTP_HOST'],
                                reverse("solutions:questiondetail", kwargs={"pk": question.pk}))


            user_email = question.user.email

            if question.user.client:
                d['client'] = question.user.client.name
                to_email = question.user.client.charged_by.supervisor.email
            else:
                to_email = 'no_replay@ntonadvisory.com'
            # text_content = plaintext.render(d)
            # html_content = htmly.render(d)
            text_content = render_to_string('email/email_client.txt',{'context':d})
            html_content = render_to_string('email/email_client.html',{'context':d})

            msg = EmailMultiAlternatives(subject, text_content, user_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            try:
                if question.user.client:
                    msg.send()
            except Exception as e:
                logger.error(e)
