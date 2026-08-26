from django.db import models

# Create your models here.
class NewsPrediction(models.Model):
    title=models.TextField(blank=True)
    text=models.TextField(blank=True)
    source=models.CharField(max_length=255,blank=True)
    url=models.URLField(blank=True)
    published_at = models.DateTimeField(null=True,blank=True)
    prediction=models.CharField(max_length=20)
    label=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction}-{self.created_at}"