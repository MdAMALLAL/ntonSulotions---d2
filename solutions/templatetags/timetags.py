from django import template
from django.utils.translation import ugettext_lazy as _
import datetime
register = template.Library()

def print_timestamp(value, arg):
    try:
        #assume, that timestamp is given in seconds with decimal point
        if not value == "":
            days = value.days
            sec = value.seconds

            if days == 1:
                return '%02d %s %02d H %02d M' % (days, _('Day'),int((sec/3600)%3600), int((sec/60)%60))
            if days > 1:
                return '%02d %s %02d H %02d M' % (days, _('Days'),int((sec/3600)%3600), int((sec/60)%60))
            return '%02d H %02d M' % (int((sec/3600)%3600), int((sec/60)%60))
        return arg

    except ValueError:
        return arg


register.filter(print_timestamp)
