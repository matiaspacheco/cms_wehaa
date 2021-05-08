from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

from tinymce.models import HTMLField
import re, datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile-pic-default.jpg',
                              upload_to='profile_pics')
    banner_image = models.ImageField(default='slider-1.jpg',
                                     upload_to='banner')
    job_title = models.CharField(max_length=100)
    bio = HTMLField()

    date_birth = models.DateField(default='1999-12-31')
    GENDER_CHOICES = (('M', 'Hombre'), ('F', 'Mujer') )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=128, verbose_name='Genero')
    country = models.CharField(max_length=100, help_text="Indique su país")

    #Social
    twitter_url = models.CharField(max_length=250, default="#",
                                   blank=True, null=True,
                                   help_text="Ingrese # si no tiene una cuenta")
    instagram_url = models.CharField(max_length=250, default="#",
                                     blank=True, null=True,
                                     help_text="Ingrese # si no tiene una cuenta")
    facebook_url = models.CharField(max_length=250, default="#",
                                    blank=True, null=True,
                                    help_text="Ingrese # si no tiene una cuenta")
    github_url = models.CharField(max_length=250, default="#",
                                  blank=True, null=True,
                                  help_text="Ingrese # si no tiene una cuenta")

    email_confirmed = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=timezone.now)

    updated_on = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.date_birth:
            return u"%s" % relativedelta.relativedelta(TODAY, self.date_birth).years
        else:
            return None

    def __str__(self):
        return f"{self.user.username}'s Profile"
