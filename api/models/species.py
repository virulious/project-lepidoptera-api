from django.db import models

from .user import User
from .genus import Genus

class Species(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=250)
  owner = models.ForeignKey(
      User,
      on_delete=models.CASCADE
  )
  genus = models.ForeignKey(
      Genus,
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"This is {self.name} and it belongs to the Genus {self.genus}"


  def as_dict(self):
    """Returns dictionary version of Genus models"""
    return {
        'id': self.id,
        'name': self.name,
        'description': self.description,
        'owner': self.owner,
        'genus': self.genus
    }
