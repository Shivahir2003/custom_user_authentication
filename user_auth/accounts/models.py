from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    GENDER_CHOICES ={
        'm':'male',
        'f':'female'
    }
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    mobile_number=models.CharField(max_length=10,null=True,blank=True,)
    forget_password_token=models.CharField(max_length=256,null=True,blank=True,default=None)
    gender=models.CharField(max_length=1,null=True,blank=True,choices=GENDER_CHOICES)
    user_image=models.ImageField(upload_to='accounts/',null=True,blank=True,default=None)

    def __str__(self):
        return str(self.user.username)

    def calculate_age(self):
        """
            get birthdate from user,
            calculate age
        """
        today = datetime.date.today()
        birth_year=self.date_of_birth.year
        return today.year - birth_year
