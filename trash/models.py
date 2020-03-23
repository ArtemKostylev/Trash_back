from django.db import models, transaction
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.utils import timezone
from datetime import datetime

def get_timestamp():
     return str(int(datetime.now().timestamp()*100))

def get_image_timestamped_path(instance, filename):
     return 'uploads/user_{0}/Img_{1}.jpg'.format(instance.user.id, get_timestamp())

class UserManager(BaseUserManager):

     def _create_user(self, phone_number, password, **extra_fields):
          if not phone_number: 
               raise ValueError('Phone number must be set')
          try:
               with transaction.atomic():
                    user = self.model(phone_number = phone_number, **extra_fields)
                    user.set_password(password)
                    user.save(using=self._db)
                    return user
          except: 
               raise
     
     def create_user(self, phone_number, password = None, **extra_fields):
          extra_fields.setdefault('is_staff', False)
          extra_fields.setdefault('is_superuser', False)
          return self._create_user(phone_number, password, **extra_fields)

     def create_superuser(self, phone_number, password, **extra_fields):
          extra_fields.setdefault('is_staff', True)
          extra_fields.setdefault('is_superuser', True)
          return self._create_user(phone_number, password, **extra_fields)
          
class User(AbstractBaseUser, PermissionsMixin):
     phone_number = models.CharField(max_length = 10, unique = True) 
     first_name = models.CharField(max_length = 30, blank = True)
     last_name = models.CharField(max_length = 30, blank = True)
     is_active = models.BooleanField(default = True)
     is_staff = models.BooleanField(default = False)
     date_joined = models.DateTimeField(default = timezone.now)

     objects = UserManager()

     USERNAME_FIELD = 'phone_number'
     REQUIRED_FIELDS = ['first_name', 'last_name']

     def save(self, *args, **kwargs):
          super(User, self).save(*args, **kwargs)
          return self

class Post(models.Model):
     text = models.CharField( max_length = 200 ) 
     latitude = models.DecimalField( max_digits = 12, decimal_places = 10 )
     longitude = models.DecimalField( max_digits = 12, decimal_places = 10 )
     created = models.DateTimeField( editable = False, auto_now_add = True)
     modified = models.DateTimeField( editable = False, null = True , auto_now=True)
     image = models.ImageField(upload_to=get_image_timestamped_path, null = True)
     #TODO Change blank and null settings in production
     author = models.ForeignKey(User, verbose_name=("User id"), on_delete=models.CASCADE, blank = True, null = True) 


     class Meta: 
          ordering = ['-created']

#TODO Save for later
class Session(models.Model):
     userId = models.ForeignKey(User, verbose_name = ("User id"),\
           on_delete = models.CASCADE)
     refreshToken = models.UUIDField(null = False)
     fingerprint = models.CharField(max_length = 100, null = False)
     ip = models.CharField(max_length = 15, null = False)
     expiresIn = models.BigIntegerField(null = False)
     created = models.DateTimeField(editable = False, auto_now_add = True)
     modified = models.DateTimeField(editable = False, auto_now = True)    

class Comment(models.Model):
     text = models.CharField(max_length=200)
     author = models.ForeignKey(User, verbose_name = ("User id"),\
          on_delete = models.CASCADE)
     created = models.DateTimeField(editable = False, auto_now_add = True)
     modified = models.DateTimeField(editable = False, auto_now = True, null = True)
     post = models.ForeignKey(Post, on_delete = models.CASCADE)
     class Meta:
          ordering = ['-created']
