from django.db import models

from .user import User

class Genus(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    # This must return a string
    return f"The Genus {self.name}"

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'name': self.name
    }
