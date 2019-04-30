from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """user topic"""
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete = models.DO_NOTHING)

    def __str__(self):
        """show the str"""
        return self.text

class Entry(models.Model):
    topic = models.ForeignKey(Topic,on_delete = models.DO_NOTHING)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """return model str"""
        return self.text[:50] + "..."
