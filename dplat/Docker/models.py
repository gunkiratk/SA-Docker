from __future__ import unicode_literals

from django.db import models
from django import forms


# Create your models here.
class Name_pass(models.Model):
	name=models.CharField(max_length=128)
	password=models.CharField(max_length=128)
	username=models.CharField(max_length=128)

class Container(models.Model):
	Cname=models.ForeignKey(
        'Name_pass',
        on_delete=models.CASCADE,
    max_length=128)	





