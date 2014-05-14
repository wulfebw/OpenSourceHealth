from django.db import models

class Group(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __unicode__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=30, unique=True)
	group = models.ForeignKey(Group, blank=True, null=True)

	def __unicode__(self):
		return self.name

	def first_letter(self):
		return self.name and self.name.upper()[0] or ''

class ModeratedCategory(models.Model):
	name = models.CharField(max_length=30)
	group = models.CharField(max_length=30, blank=True, null=True)

	def __unicode__(self):
		return self.name

