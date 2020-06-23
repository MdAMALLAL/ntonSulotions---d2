from django.urls import  reverse_lazy
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from clients import models as client

class UserManager(AbstractUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(_('Display Name'),unique=True, max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    tel = models.CharField(blank=True, max_length=40,verbose_name=_('Telephone'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('Consultant'), default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    client = models.ForeignKey(client.Client, null=True, blank=True, related_name="users",on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def __str__(self):
        return "@{}".format(self.username)

    def get_absolute_url(self):
        return reverse_lazy("accounts:edit", kwargs={"username": self.username})

    def get_consultant(self):
        return User.objects.filter(is_staff = True)

    def add_notification(self, description, url):
        notification = Notification.objects.create(user=self, description = description, url=url)
        notification.save

    def get_notification(self):
        querySet = Notification.objects.filter(user=self).update(new=False, seen= timezone.now())
        querySet = Notification.objects.filter(user=self)
        return querySet
    def get_last_10_notification(self):
        querySet = Notification.objects.filter(user=self).update(new=False)
        querySet = Notification.objects.filter(user=self)[:10]
        return querySet

    def get_new_notification(self):
        return Notification.objects.filter(user=self, new=True )

    def get_notification_count(self):
        return Notification.objects.filter(user=self, seen__isnull=True).count()

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    description = models.TextField()
    url = models.CharField(max_length = 55)
    new = models.BooleanField(default=True)
    seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description

    def viewed(self):
        self.seen = timezone.now()
        return self.save()

    def displayed(self):
        self.new = False

    class Meta:
        ordering = ["-date"]
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
