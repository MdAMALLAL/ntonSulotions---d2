from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.mail import BadHeaderError, send_mail
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
        ('RP', _('Answered')),
        ('DS', _('Deactiveted')),
        )


    def content_file_name(instance, filename):
        filename = "%s__%s" % (uuid.uuid4(),filename)
        return os.path.join('images', str(instance.user.id), filename)

    user = models.ForeignKey(User,null=True, related_name="tickets",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    titre = models.CharField(max_length=200)

    image = models.ImageField(blank=True,null=True, upload_to=content_file_name)

    priorite=models.CharField(max_length=1,choices=Priorite,default='F',)
    status = models.CharField(max_length=2,choices=Status,default='OV',)
    #categorie = models.CharField(max_length=3,choices=Categorie,default='AUT',)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='quesions',)
    souscategorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, related_name='quesions',)

    description = models.TextField()


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
            return reverse("solutions:questiondetail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ["-created_at"]

    # def save(self, *args, **kwargs):
    #     subject = self.titre
    #     message = self.description + ' ' + get_absolute_url(self)
    #
    #     from_email = self.user.email
    #     send_mail(subject, message, from_email, ['no_replay@ntonadvisory.com'])
    #
    #     subject = self.titre
    #     message = self.description
    #     from_email = 'admin@example.com'
    #     send_mail(subject, message, from_email, [self.user.email,])
    #
    #     super().save(*args, **kwargs)



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
