from enum import Enum
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy
from django.conf import settings

User = settings.AUTH_USER_MODEL



# Create your models here.
class Question (models.Model):
####################################
###          Categorie           ###
####################################
    class Categorie(Enum):
        RESEAU='RES', gettext_lazy('Network')
        MATERIEL='MAT', gettext_lazy('Hardware')
        LOGICIEL='lOG', gettext_lazy('Software')
        AUTRE='AUT', gettext_lazy('Other')
####################################
###           Priorite           ###
####################################
    class Priorite(Enum):
        FAIBLE='F', gettext_lazy('Low')
        MOYENNE='M', gettext_lazy('Medium')
        HOUTE='H', gettext_lazy('Height')
        URGENT='U', gettext_lazy('Urgent')
####################################
###           Status             ###
####################################
    class Status(Enum):
        ENATTENTE='EA', gettext_lazy('Waiting')
        RESOLU='RS', gettext_lazy('Resolved')
        OUVERT='OV', gettext_lazy('Open')
        FERME='FR', gettext_lazy('Closed')
        FEFUSE='RF', gettext_lazy('Refused')
        ANNULE='AN', gettext_lazy('Canceled')
        REPONDE='RP', gettext_lazy('Answered')
        DESACTIVE='DS', gettext_lazy('Deactiveted')


    user = models.ForeignKey(User,null=True, related_name="tickets",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    objet = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(blank=True,null=True, upload_to='images/')

    priorite=models.CharField(max_length=1,choices=Priorite, default=Priorite.FAIBLE,)
    status = models.CharField(max_length=2,choices=Status, default=Status.OUVERT,)
    categorie = models.CharField(max_length=3,choices=Categorie, default=Categorie.AUTRE,)

    def get_priorite(self):
        return self.Priorite(self.priorite).label

    class Color(Enum):
        secondary='F', gettext_lazy('secondary')
        primary='M', gettext_lazy('primary')
        success='H', gettext_lazy('success')
        denger='U', gettext_lazy('danger')


    def get_color(self):
        return self.Color(self.priorite).label

    def get_status(self):
        return self.Status(self.status).label

    def get_categorie(self):
        return self.Categorie(self.categorie).label

    def get_absolute_url(self):
            return reverse("solutions:questiondetail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.objet

    class Meta:
        ordering = ["-created_at"]



class Reponce(models.Model):
    user = models.ForeignKey(User,null=True, related_name="reponces",on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    question = models.ForeignKey(Question,null=True, related_name="reponces",on_delete=models.SET_NULL)
    image = models.ImageField(null=True,blank=True, upload_to='images/')

    def __str__(self):
        return self.description
