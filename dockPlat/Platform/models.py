from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Container(models.Model):
	author = models.ForeignKey(User)
	c_name = models.CharField(max_length=150, null=True)
	image_id = models.CharField(max_length=150, null=True)
	image = models.CharField(max_length=150, null=True)

	def __str__(self):
		return str(self.c_name)
