from django.db import models
from django.contrib.auth.models import User
import random

from colorful.fields import RGBColorField
from uuidfield import UUIDField

class Tag(models.Model):

    def randomColor():
        decimalValue = random.randint(0,16777215) #16777215 = (16^6)-1, or #FFFFFF in Hex
        hexValue = hex(decimalValue) #Convert to hex... prefixed with 0x, though.
        htmlColour = str(hexValue)[2:] #Convert to String, Strip hexValue of first 2 chars, leaving with 6 digit hex value
        return htmlColour

    #owner = models.ForeignKey(User) #(Not sure if we want this...)
    name = models.CharField(max_length=12) #12 seems like a good length? Maybe this should be read from a settings file/model... ah well, we can sort that in a future release ;)
    labelForeground = RGBColorField(default=randomColor()) #todo: make sure foreground and background don't clash (using magic)
    labelBackground = RGBColorField(default=randomColor())
    creationDate = models.DateTimeField(auto_now_add=True) #Now. Might as well log this.

class Category(models.Model):
    name = models.CharField(max_length=15) #read from config file/model?

class Gif(models.Model):
    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)
    gifFile = models.FileField(upload_to="gifDir/")
