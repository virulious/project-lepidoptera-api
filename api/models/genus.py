from django.db import models

from .user import User

class Genera(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    # This must return a string
    return f"The Genera {self.name}"

  def as_dict(self):
    """Returns dictionary version of Genera models"""
    return {
        'id': self.id,
        'name': self.name
    }
