from django.db import models

# Create your models here.

class Employee(models.Model):
    eno = models.IntegerField()
    ename = models.CharField(max_length=20)
    esal = models.FloatField()
    eadd = models.CharField(max_length=20)
    def __str__(self):
        return self.ename
