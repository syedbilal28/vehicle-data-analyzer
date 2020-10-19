from django.db import models

# Create your models here.
class Car(models.Model):
    class Meta:
        db_table="Car"
        managed=False
    # Model= models.CharField(max_length=20)
    # Make=models.CharField(max_length=20)
    # Year=models.CharField(max_length=4)
    # Views_Per_Day= models.FloatField()
    # Views_Per_Day_1= models.FloatField()
    # Views_Per_Day_2= models.FloatField()
    # Views_Per_Day_3= models.FloatField()
    # Views_Per_Day_4= models.FloatField()
    # Views=models.IntegerField()
    # DaysOnline=models.FloatField()
class Car_Days(models.Model):
    class Meta:
        db_table="Car_Days"
        managed=False

    # Model = models.CharField(max_length=20)
    # Make = models.CharField(max_length=20)
    # Year = models.CharField(max_length=4)
    # Days_Online = models.FloatField()
    # Days_Online_1 = models.FloatField()
    # Days_Online_2 = models.FloatField()
    # Days_Online_3 = models.FloatField()
    # Days_Online_4 = models.FloatField()
