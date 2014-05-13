from django.db import models

class Group(models.Model):
	name	= models.CharField(max_length = 30, unique = True)

	def __unicode__(self):
		return self.name

class Category(models.Model):
	name 	= models.CharField(max_length = 30, unique = True)
	group 	= models.ForeignKey(Group)

	def __unicode__(self):
		return self.name

	def first_letter(self):
		return self.name and self.name.upper()[0] or ''

