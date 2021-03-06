from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
import datetime
import uuid
User = settings.AUTH_USER_MODEL



# Create your models here.
class Categorie(models.Model):
    """Django data model Categorie"""
    name = models.CharField(blank=True, max_length=100)
    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return str(self.name)

class SousCategorie(models.Model):
    """Django data model SousCategorie"""
    name = models.CharField(blank=True, max_length=100)
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, related_name='SousCategories',)
    class Meta:
        verbose_name = 'SousCategorie'
        verbose_name_plural = 'SousCategories'
    def __str__(self):
        return str(self.categorie.name + '/'+self.name)


class Question(models.Model):

###           Priorite           ###
    Priorite=(
        ('F', _('Low')),
        ('M', _('Medium')),
        ('H', _('Height')),
        ('U', _('Urgent')),
        )
###           Status             ###
    Status= (
        ('EA', _('Waiting')),
        ('RS', _('Resolved')),
        ('OV', _('Open')),
        ('FR', _('Closed')),
        ('RF', _('Refused')),
        ('AN', _('Canceled')),
        ('DS', _('Deactiveted')),
        )


    def content_file_name(instance, filename):
        filename = "%s__%s" % (uuid.uuid4().hex[:6].upper(),filename)
        return os.path.join('images', str(instance.user.id), filename)
    def ref():
        this_year = datetime.date.today().year
        no = Question.objects.filter(created_at__year=this_year).count()
        if no == None:
            return '{0}-{1}'.format(this_year, 1)
        else:
            return '{0}-{1}'.format(this_year, no + 1)


    user = models.ForeignKey(User,null=True, related_name="tickets",on_delete=models.SET_NULL)
    ref = models.CharField(default=ref, unique=True, editable=False,  max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    titre = models.CharField(max_length=200)
    image = models.ImageField(blank=True,null=True, upload_to=content_file_name)
    priorite=models.CharField(max_length=1,choices=Priorite,default='F',)
    status = models.CharField(max_length=2,choices=Status,default='OV',)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='quesions',)
    souscategorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, related_name='quesions',)
    description = models.TextField(blank=True,verbose_name=_('comment'))
    viwed_at = models.DateTimeField(blank=True,null=True)
    time_to_view = models.DurationField(blank=True,null=True,verbose_name=_('time to view'))
    charged_by = models.ForeignKey(User,null=True, related_name="charged_tickets",on_delete=models.SET_NULL)
    first_react_at = models.DateTimeField(blank=True,null=True)
    time_to_react = models.DurationField(blank=True,null=True,verbose_name=_('time to react'))
    resolved_at = models.DateTimeField(blank=True,null=True)
    time_to_resolv = models.DurationField(blank=True,null=True,verbose_name=_('Time to resolve'))
    last_action = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.viwed_at:
            self.time_to_view = self.viwed_at - self.created_at
        if self.first_react_at:
            self.time_to_react = self.first_react_at - self.created_at
        if self.resolved_at:
            self.time_to_resolv = self.resolved_at - self.created_at



        super().save(*args, **kwargs)




    def date_to_string(self,date, string, *args):
        if date:
            days = date.days
            sec = date.seconds
            if days == 1:
                return '%02d %s %02d H %02d M' % (days, _('Day'),int((sec/3600)%3600), int((sec/60)%60))
            if days > 1:
                return '%02d %s %02d H %02d M' % (days, _('Days'),int((sec/3600)%3600), int((sec/60)%60))
            return '%02d H %02d M' % (int((sec/3600)%3600), int((sec/60)%60))
        return string

    def date_to_minute(self, date):
        return date.days * 24  + date.seconds / 3600

    def get_time_to_resolv(self):
        string = _("Not resolved yet")
        return self.date_to_string(self.time_to_resolv, string)

    def get_time_to_view(self):
        string = _("Not viewed yet")

        return self.date_to_string(self.time_to_view, string)

    def get_time_to_react(self):
        string = _("Not reacted yet")

        return self.date_to_string(self.time_to_react, string)


    Color = {}
    Color['F'] = 'secondary'
    Color['M'] = 'primary'
    Color['H'] = 'success'
    Color['U'] = 'danger'

    def get_color(self):
        return self.Color.get(self.priorite)

    def get_categorie(self):
        return self.categorie.name + '/' + self.souscategorie.name

    def get_absolute_url(self):
            return reverse_lazy("solutions:questiondetail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')




class Reponce(models.Model):
    Status= (
        ('EA', _('Waiting')),
        ('RS', _('Resolved')),
        ('FR', _('Closed')),
        ('RF', _('Refused')),
        ('AN', _('Canceled')),
        )
    user = models.ForeignKey(User,null=True, related_name="reponces",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,)
    description = models.TextField(null=True)
    question = models.ForeignKey(Question,null=True, related_name="reponces",on_delete=models.SET_NULL)
    image = models.ImageField(null=True,blank=True, upload_to='images/')
    status = models.CharField(max_length=2,choices=Status,default='EA',)

    def __str__(self):
        return self.description

# class notification(models.Model):
#     user = models.ForeignKey(User, related_name='notifications', on_delete=models.EN_CASCADE)
#     date = models.DateTimeField(auto_now=True)
#     description = models.TextField()
#     url = models.CharField()
#     seen = models.BooleanField(blank=True, default=False-*+)
#
#     def __str__(self):
#         return self.description
