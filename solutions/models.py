from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
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
        filename = "%s__%s" % (uuid.uuid4(),filename)
        return os.path.join('images', str(instance.user.id), filename)

    user = models.ForeignKey(User,null=True, related_name="tickets",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    titre = models.CharField(max_length=200)

    image = models.ImageField(blank=True,null=True, upload_to=content_file_name)

    priorite=models.CharField(max_length=1,choices=Priorite,default='F',)
    status = models.CharField(max_length=2,choices=Status,default='OV',)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='quesions',)
    souscategorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, related_name='quesions',)

    description = models.TextField()
    viwed_at = models.DateTimeField(blank=True,null=True)
    time_to_view = models.DurationField(blank=True,null=True,verbose_name=_('time to view'))
    first_react_at = models.DateTimeField(blank=True,null=True)
    time_to_react = models.DurationField(blank=True,null=True,verbose_name=_('time to react'))
    resolved_at = models.DateTimeField(blank=True,null=True)
    time_to_resolv = models.DurationField(blank=True,null=True,verbose_name=_('time to resolv'))
    last_action = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.viwed_at:
            self.time_to_view = self.viwed_at - self.created_at
        if self.first_react_at:
            self.time_to_react = self.first_react_at - self.created_at
        if self.resolved_at:
            self.time_to_resolv = self.resolved_at - self.created_at



        super().save(*args, **kwargs)





    def get_time_to_resolv(self):
        if self.time_to_resolv:
            sec = self.time_to_resolv.seconds
            return '%02d:%02d' % (int((sec/3600)%3600), int((sec/60)%60))
        return _('Not Resolved Yet')
    def get_time_to_view(self):
        if self.time_to_view:
            sec = self.time_to_view.seconds
            return '%02d:%02d' % (int((sec/3600)%3600), int((sec/60)%60))
        return _('Not Viewed Yet')
    def get_time_to_react(self):
        if self.time_to_react:
            sec = self.time_to_react.seconds
            return '%02d:%02d' % (int((sec/3600)%3600), int((sec/60)%60))
        return _('Not Reacted Yet')

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
    user = models.ForeignKey(User,null=True, related_name="reponces",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True,)
    description = models.TextField()
    question = models.ForeignKey(Question,null=True, related_name="reponces",on_delete=models.SET_NULL)
    image = models.ImageField(null=True,blank=True, upload_to='images/')

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
