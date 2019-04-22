from django.db import models

# Create your models here.

class table_a(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField('date created')

    def __str__(self):
        return self.title 