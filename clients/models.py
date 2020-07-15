from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.conf import settings
from solutions.models import Question

User = settings.AUTH_USER_MODEL

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    address = models.TextField(blank=True,verbose_name=_('Address'))
    tel = models.CharField(blank=True, max_length=40,verbose_name=_('Telephone'))
    url = models.URLField(blank=True, verbose_name=_('Web site'))
    email = models.EmailField(verbose_name=_('DSI Email'))
    contact = models.CharField(blank=True,max_length=100,verbose_name=_('Contact'))
    contact_tel = models.CharField(blank=True,max_length=100,verbose_name=_("Contact's tel"))
    contact_email = models.EmailField(blank=True,verbose_name=_('Contact Email'))
    charged_by = models.ForeignKey(User,null=True, related_name="charged_clients",verbose_name=_('Resposable'),on_delete=models.SET_NULL)
    slug = models.SlugField(allow_unicode=True, unique=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.validate_unique()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('clients:detail',  kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]
    def tickets(self):
        return Question.objects.filter(user__client__slug = self.slug)
    def tickets_open(self):
        return Question.objects.filter(user__client__slug = self.slug, status='OV')
    def tickets_waiting(self):
        return Question.objects.filter(user__client__slug = self.slug, status='EA')
    def tickets_resolved(self):
        return Question.objects.filter(user__client__slug = self.slug, status='RS')
    def tickets_Closed(self):
        return Question.objects.filter(user__client__slug = self.slug, status='FR')
    def tickets_Refused(self):
        return Question.objects.filter(user__client__slug = self.slug, status='RF')
