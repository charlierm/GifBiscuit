from django.db import models
from django.contrib.auth.models import User

from Colour.fields import ColorField
from uuidfield import UUIDField

class Tag(model.Models):

    def randomColor(self):
        decimalValue = random.randint(0,16777215) #16777215 = (16^6)-1, or #FFFFFF in Hex
        hexValue = hex(decimalValue) #Convert to hex... prefixed with 0x, though.
        htmlColour = str(hexValue)[2:] #Convert to String, Strip hexValue of first 2 chars, leaving with 6 digit hex value
        return htmlColor

    #owner = models.ForeignKey(User) #(Not sure if we want this...)
    name = models.CharField(max_length=12) #12 seems like a good length? Maybe this should be read from a settings file/model... ah well, we can sort that in a future release ;)
    labelForeground = ColorField(defalut=self.randomColor()) #todo: make sure foreground and background don't clash (using magic)
    labelBackground = ColorField(default=self.randomColor())
    creationDate = models.DateTimeField(auto_add_now=True) #Now. Might as well log this.

class Category(model.Models):
    name = models.CharField(max_length=15) #read from config file/model?

class Gif(model.Models):
    owner = models.ForeignKey(User)
    tags = models.ManyToMany(Tag)
    category = models.ForeignKey(Category)
    gifFile = models.FileField(upload_to="gifDir/")
