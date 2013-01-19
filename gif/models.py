from colorful.fields import RGBColorField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
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
        
class UserManager(BaseUserManager):
    """
    Extends Djangos BaseUserManager class. 
    
    Facilitates using Django authentication.
    """
    
    def create_user(self, username, email_address, password):
        """
        Factory method returning a new instance of the User class with the supplied details.
        
        @param username The username of the new user.
        @param email_address The email address of the new user.
        @param password The users set password, before hashing.
        
        @return User Returns the newly created User object.    
        """
        if (not username or not email_address):
            raise ValueError('User must have username and email_address. %s, %s'
                             ) % (username. email_address)
                             
        user = self.model(username=username,
                          email_address=email_address
                          )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email_address, password):
        """
        Factory method returning a new instance of the User class 
        with the supplied details as a superuser.
        
        @param username The username of the new user.
        @param email_address The email address of the new user.
        @param password The users set password, before hashing.
        
        @return User Returns the newly created User object.  
        """  
        
        if (not username or not email_address):
            raise ValueError('User must have username and email_address. %s, %s'
                             ) % (username. email_address)
                             
        user = self.model(username=username,
                          email_address=email_address
                          )
        user.set_password(password)
        user.is_superuser = True
        user.save() 
        return user
             
        
class User(AbstractBaseUser, Base):
    """
    Represents a user of the system. 
    """
    ##The username of the User
    username = models.CharField(max_length=50, unique=True)
    ##Email address registered with the User
    email_address = models.EmailField(max_length=75)
    ##Whether the user account is active
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email_address']
    
    objects = UserManager()
    
    def add_user_field(self, UserField):
        """
        Adds a UserField object to the User
        
        @param UserField The UserField object to set as belonging to the user.
        @return UserField Returns the UserField added. 
        @throws UserDataException
        """
        return
    
    def get_full_name(self):
        """
        Returns the users username.
        """
        return self.username
    
    def get_short_name(self):
        """
        Returns the users username.
        """
        return self.username

class Tag(models.Model):
    
    #owner = models.ForeignKey(User) #(Not sure if we want this...)
    name = models.CharField(max_length=12) #12 seems like a good length? Maybe this should be read from a settings file/model... ah well, we can sort that in a future release ;)
    labelForeground = RGBColorField(default=randomColor()) #todo: make sure foreground and background don't clash (using magic)
    labelBackground = RGBColorField(default=randomColor())
    creationDate = models.DateTimeField(auto_now_add=True) #Now. Might as well log this.

    def randomColor():
        decimalValue = random.randint(0,16777215) #16777215 = (16^6)-1, or #FFFFFF in Hex
        hexValue = hex(decimalValue) #Convert to hex... prefixed with 0x, though.
        htmlColour = str(hexValue)[2:] #Convert to String, Strip hexValue of first 2 chars, leaving with 6 digit hex value
        return htmlColour

class Category(models.Model):
    name = models.CharField(max_length=15) #read from config file/model?

class Gif(models.Model):
    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)
    gifFile = models.FileField(upload_to="gifDir/")
