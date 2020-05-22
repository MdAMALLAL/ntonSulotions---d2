from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100,verbose_name=_('Name'))
    address = models.TextField(blank=True,verbose_name=_('Adress'))
    tel = models.CharField(blank=True, max_length=40,verbose_name=_('Telephone'))
    url = models.URLField(blank=True, verbose_name=_('Web site'))
    email = models.EmailField(verbose_name=_('Email'))
    comment = models.TextField(blank=True,verbose_name=_('Comment'))
    signed = models.DateField(null=True,blank=True,verbose_name=_('Contract signed on'))
    slug = models.SlugField(allow_unicode=True, unique=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("clients:detail", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]
