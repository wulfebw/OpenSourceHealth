from django.db import models
from categories.models import *
from django.contrib.auth.models import User
import requests
import json
import datetime


class Project(models.Model):
	name 				= models.CharField(max_length = 30, unique = True)
	#creator				= models.ForeignKey(User)
	github_repo			= models.CharField(max_length = 100)
	category			= models.ForeignKey(Category, blank = True, null = True)
	rating				= models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, null = True)
	description 		= models.TextField(blank = True)	
	website_url 		= models.URLField(max_length = 100, blank = True)
	documentation_url 	= models.URLField(max_length = 100, blank = True)
	bug_tracker_url		= models.URLField(max_length = 100, blank = True)
	mailing_list_url	= models.URLField(max_length = 100, blank = True)
	github_contributors	= models.IntegerField(blank = True, null = True)
	github_watchers		= models.IntegerField(blank = True, null = True)
	github_forks		= models.IntegerField(blank = True, null = True)
	github_issues		= models.IntegerField(blank = True, null = True)
	last_commit_date	= models.DateField(blank = True, null = True)
	first_commit_date	= models.DateField(blank = True, null = True)

	def __unicode__(self):
		return self.name

	""" Method used to group projects in the template using 'regroup' """
	def first_letter(self):
		return self.name[0].upper() or ''

	""" Updates general information about a project (watchers, forks, issues) """
	def update_general(self):
		r = requests.get('https://api.github.com/repos/{0}'.format(self.github_repo))
		if r.ok:
			info = r.json()
			self.github_watchers = info[u'watchers']
			self.github_forks = info[u'forks']
			self.github_issues = info[u'open_issues_count']

	""" Updates contributor information about a project (# of contributors) """
	def update_contribs(self):		
		r = requests.get('https://api.github.com/repos/{0}/stats/contributors'.format(self.github_repo))
		if r.status_code == 200 or r.status_code == 202:
			info = r.json()
			self.github_contributors = len(info)
			# could get the top contributors here
			# r.json()[0][u'author'][u'login'] gives login of first author
		# elif r.status_code == 204:	
		# 	self.github_contributors = 0
		
	""" Updates commit information about a project (most recent commit) """
	def update_commits(self):
		r = requests.get('https://api.github.com/repos/{0}/commits'.format(self.github_repo))
		if r.status_code == 200 or r.status_code == 202:
			info = r.json()
			if len(info) > 0:
				# get the date of the last commit
				date_str = str(info[0][u'commit'][u'committer'][u'date'])
				year = int(date_str[0:4])
				month = int(date_str[5:7])
				day = int(date_str[8:10])
				self.last_commit_date = datetime.date(year, month, day)

	def update_states(self):
		r = requests.get('https://api.github.com/repos/{0}/stats/commit_activity'.format(self.github_repo))
		if r.status_code == 200 or r.status_code == 202:
			info = r.json()
			activity = []
			if len(info) < 8:
				activity = info
			else:
				activity = info[0:8]
			commit_count = 0
			for week in activity:
				commit_count = commit_count + week[u'total']
			# stopped here, but you this gives you total commits for past 2 months
			
	def update_websites(self):
		if not self.website_url:
			website_url = 'github.com/{0}'.format(self.github_repo)
			documentation_url = website_url 
			bug_tracker_url = website_url + '/issues'
			mailing_list_url = website_url
			
				
	""" Updates a projects rating """
	def update_rating(self):

		score = self.github_watchers + self.github_forks
		top_score = 1000 # placeholder: this depends on the projects on the site
		self.rating = float(score) / top_score

	""" Method calling all the update functions """
	def update_project_info(self):
		self.update_general()
		self.update_contribs()
		self.update_commits()
		self.update_websites()
		self.update_rating()
		self.save()



""" This class is used when a project is edited or created
	it must then be confirmed by a moderator through the 
	admin interface. After confirmation, this model is 
	converted to the complete Project model.
"""
class ModeratedProject(models.Model):
	name 				= models.CharField(max_length = 30)
	github_repo			= models.CharField(max_length = 100)
	category			= models.CharField(max_length = 100)
	comments			= models.TextField(blank = True)
	existing_project	= models.ForeignKey(Project, blank = True, null = True)

	def __unicode__(self):
		return self.name






