from colorful.fields import RGBColorField
from django.db import models
from django.contrib.auth.models import User
from utils import Utils
import random, uuid

class Base(models.Model):
    """
    Base class containing common properties and methods for models.
    
    All models will extend this class.
    """
    
    """UUID of the object, as String"""
    uuid = models.CharField(max_length=36, primary_key=True)
    
    def save(self, *args, **kwargs):
        """
        Overrides the django.model.save() method to add a random UUID
        to new objects before they are persisted to the DB.
        """
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super(Base, self).save(*args, **kwargs)
        
    class Meta:
        app_label = "gif"
        abstract = True

class Tag(models.Model):
    
    name = models.CharField(max_length=12) #TODO:12 seems like a good length? Maybe this should be read from a settings file/model... ah well, we can sort that in a future release ;)
    foreground_colour = RGBColorField() #TODO: make sure foreground and background don't clash (using magic)
    background_colour = RGBColorField()
    date_created = models.DateTimeField(auto_now_add=True) #Now. Might as well log this.

    def __unicode__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        if (self.background_colour == '' and self.foreground_colour == ''):
        	colours = Utils.get_colour_pair()
        	self.background_colour = colours[0]
        	self.foreground_colour = colours[1]

class Category(models.Model):
    name = models.CharField(max_length=15) #read from config file/model
    
    def __unicode__(self):
        return self.name

class Gif(models.Model):
    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)
    gifFile = models.FileField(upload_to="gifDir/")

    def __unicode__(self):
        return self.gifFile.url
