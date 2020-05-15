from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from django.contrib.auth import get_user_model
User = get_user_model()



# Create your models here.
class Question(models.Model):
####################################
###          Categorie           ###
####################################
    Categorie=(
        ('RES', _('Network')),
        ('MAT', _('Hardware')),
        ('lOG', _('Software')),
        ('AUT', _('Other')),
        )
####################################
###           Priorite           ###
####################################
    Priorite=(
        ('F', _('Low')),
        ('M', _('Medium')),
        ('H', _('Height')),
        ('U', _('Urgent')),
        )
####################################
###           Status             ###
####################################
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

    user = models.ForeignKey(User,null=True, related_name="tickets",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(blank=True,null=True, upload_to='images/')

    priorite=models.CharField(max_length=1,choices=Priorite,default='F',)
    status = models.CharField(max_length=2,choices=Status,default='OV',)
    categorie = models.CharField(max_length=3,choices=Categorie,default='AUT',)


    Color = {}
    Color['F'] = 'secondary'
    Color['M'] = 'primary'
    Color['H'] = 'success'
    Color['U'] = 'danger'

    def get_color(self):
        return self.Color.get(self.priorite)


    def get_absolute_url(self):
            return reverse("solutions:questiondetail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ["-created_at"]



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
