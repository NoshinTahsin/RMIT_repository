from django.db import models

# Create your models here.
class Product (models.Model):

	title = models.CharField(max_length=130)
	description = models.TextField(blank=True, null=True)
	price = models.FloatField()
	title = models.TextField()
	summary = models.TextField(default='this is cool')
	featured = models.TextField(default='ashlam') 
	sample_file = models.FileField 