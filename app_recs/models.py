from django.db import models

# Create your models here.
class Recommend(models.Model):
    id = models.AutoField(primary_key=True)
    Current = models.CharField(max_length=16)
    League = models.CharField(max_length=16)
    Time1 = models.DateTimeField()
    Host = models.CharField(max_length=64)
    OddStake = models.CharField(max_length=64)
    Guest = models.CharField(max_length=64)
    Prefer = models.CharField(max_length=64)
    Odds = models.FloatField()
    Result = models.CharField(max_length=16)
    PreferResult = models.IntegerField(default=0)
    Time2 = models.DateTimeField()
    Person = models.CharField(max_length=32)

    class Meta:
        unique_together = ("Current", "League", "Time1", "Host", "OddStake", "Guest", "Prefer", "Odds", "Time2", "Person")
