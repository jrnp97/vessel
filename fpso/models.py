from django.db import models

# Create your models here.


class Vessel(models.Model):
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.code}'


class Equipment(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    vessel = models.ForeignKey(Vessel, on_delete=models.PROTECT, related_name='equipment')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        unique_together = ('vessel', 'code')

    def __str__(self):
        return f'{self.vessel}: {self.code} - {self.name}'


