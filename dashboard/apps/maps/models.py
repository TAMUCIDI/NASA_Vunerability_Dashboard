from django.db import models

# Create your models here.
class Maps(models.Model):
    Speed90 = models.FloatField()
    ShorelineDist = models.FloatField()
    MilitaryDist = models.FloatField()
    Landing19 = models.FloatField()

    def publish(self):
        self.save()
    
    class Meta:
        verbose_name_plural = "Maps"