from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Container(models.Model):
	user = User.objects.get(username='gunkirat1')
	author=models.ForeignKey(User, default=user)
	c_name = models.CharField(max_length=150, unique=True, null=True)
	image_id = models.CharField(max_length=150, unique=True, null=True)

	def __str__(self):
		return str(self.c_name)





