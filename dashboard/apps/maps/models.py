from django.db import models

# Create your models here.
class Maps(models.Model):
    Speed90Weight = models.FloatField()
    ShorelineDistWeight = models.FloatField()
    MilitaryDistWeight = models.FloatField()
    ProtectedAreaDistWeight = models.FloatField()
    Landing19Weight = models.FloatField()
    Landing19Weight = models.FloatField()
    Landing19Weight = models.FloatField()

    def publish(self):
        self.save()
    
    class Meta:
        verbose_name_plural = "Maps"