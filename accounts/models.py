from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
import uuid
# Create your models here.
class User(AbstractUser):
   id= models.UUIDField(primary_key=True,default=uuid.uuid4, editable =False)
   email= models.EmailField(unique=True)
   full_name= models.CharField(max_length=256,blank=True)
   avatar_url =models.URLField(blank=True, null =True)

   def __str__(self):
      return self.username or self.email
