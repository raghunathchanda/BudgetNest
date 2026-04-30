from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class FamilyMembers(models.Model): # contains family details
    familyLead = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    age = models.IntegerField()
    income = models.FloatField(max_length=5000000000000000)

    def __str__(self):# what is str
        return self.firstname # returning first name of family member

