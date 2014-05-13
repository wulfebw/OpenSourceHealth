from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
import requests
import json

import logging
logger = logging.getLogger('log')

""" Extension of the user model for use in profiles"""
class UserProfile (models.Model):
	user = models.OneToOneField(User)
	favorite_projects = models.ManyToManyField(Project, blank = True, null = True)
	github_repos = models.IntegerField(blank = True, null = True)
	github_gists = models.IntegerField(blank = True, null = True)
	receive_email = models.BooleanField()

	def __unicode__(self):
		return self.user.username

	""" Method updating user's gist and repo counts """
	def update_user_info(self):
		r = requests.get('https://api.github.com/users/{0}'.format(self.user.username))
		logger.info(r.json())
		if r.ok:
			info = r.json()
			self.github_repos = info[u'public_repos']
			self.github_gists = info[u'public_gists']
			self.save()



