from django.db import models
import datetime
from django import forms
from django.core.validators import URLValidator
from django.conf import settings

# Create your models here.

class WordList(models.Model):
    """
        Simply to hold the word list and if the word was used as key to shorten any url.
    """
    word = models.CharField(max_length=200, unique=True)
    is_used = models.BooleanField(default=False)

    def __unicode__(self):
        return self.word
        
class PairedUrl(models.Model):
    """
        In this model, we save the generated key for the url submitted.
    """
    key_generated = models.OneToOneField(WordList, primary_key=True)
    url = models.URLField(unique=True, validators=[URLValidator()])
    cdate = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.url  + '---> ' + self.key_generated.word


    def save(self, *args, **kwargs):
        """
            Save method was overriden in order make the generated key's status "is_used" to "True".
        """
        self.key_generated.is_used = True
        self.key_generated.save()
        super(PairedUrl, self).save(*args, **kwargs)

    def short_url(self):
        return settings.SITE_BASE_URL + self.to_base62()