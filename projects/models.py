from django.db import models
from categories.models import *
from django.contrib.auth.models import User
import requests
import json
import datetime


class Project(models.Model):
	"""
	Abstract base class for the other project types
	"""


	# The website url is the only piece of information required originally
	# e.g., 
	#	https://github.com/wulfebw/OpenSourceHealth
	#	http://sourceforge.net/projects/opensmile/
	#	https://bitbucket.org/pypy/pypy

	website_url = models.URLField(max_length = 100)

	name = models.CharField(max_length = 30, unique = True)
	category = models.ForeignKey(Category, blank = True, null = True)
	rating = models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, null = True)
	description = models.TextField(blank = True, null = True)	
	activity_level = models.IntegerField(blank = True, null = True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return self.name

	def first_letter(self):
		""" 
		Method used to group projects in the template using 'regroup' 
		"""

		return self.name[0].upper() or ''



""" 
------
GitHub 
------
"""

class GitHubProject(Project):
	"""
	Github project class
	"""

	github_repo	= models.CharField(max_length = 100, unique = True, blank = True, null = True)
	github_contributors	= models.IntegerField(blank = True, null = True)
	github_watchers = models.IntegerField(blank = True, null = True)
	github_forks = models.IntegerField(blank = True, null = True)
	github_issues = models.IntegerField(blank = True, null = True)


	def collect_basic(self):
		"""
		Gathers basic information about a github project (name, category, description, repo)
		"""

		self.github_repo = self.extract_github_repo()
		self.name = self.extract_name()
		self.category = self.predict_category()
		self.description = self.get_description()


	def update_watchers_forks_issues(self):
		""" 
		Updates general information about a project (watchers, forks, issues)
		"""
		try:
			r = requests.get('https://api.github.com/repos/{0}'.format(self.github_repo))
			if r.ok:
				info = r.json()
				self.github_watchers = info[u'watchers']
				self.github_forks = info[u'forks']
				self.github_issues = info[u'open_issues_count']
		except Exception as e:
			logger.info(e)


	def update_contributors(self):		
		""" 
		Updates contributor information about a project (# of contributors) 
		"""

		try:
			r = requests.get('https://api.github.com/repos/{0}/stats/contributors'.format(self.github_repo))
			if r.ok:
				info = r.json()
				self.github_contributors = len(info)
		except Exception as e:
			logger.info(e)

		
	def update_commits(self):
		""" 
		Updates commit information about a project (most recent commit) 
		"""

		try:
			r = requests.get('https://api.github.com/repos/{0}/commits'.format(self.github_repo))
			if r.ok:
				info = r.json()
				if len(info) > 0:
					# get the date of the last commit
					date_str = str(info[0][u'commit'][u'committer'][u'date'])
					year = int(date_str[0:4])
					month = int(date_str[5:7])
					day = int(date_str[8:10])
					self.last_commit_date = datetime.date(year, month, day)
		except Exception as e:
			logger.info(e)


	def update_activity_level(self):
		"""
		Updates the activity level of a project
		"""

		try:
			r = requests.get('https://api.github.com/repos/{0}/stats/commit_activity'.format(self.github_repo))
			if r.ok:
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
		except Exception as e:
			logger.info(e)

							
	def update_rating(self):
		""" 
		Updates the project rating
		"""

		score = self.github_watchers + self.github_forks
		top_score = 1000 # placeholder: this depends on the projects on the site
		self.rating = float(score) / top_score


	def update_project_info(self):
		""" 
		Method calling all the update functions 
		"""

		self.update_watchers_forks_issues()
		self.update_contributors()
		self.update_commits()
		self.update_rating()
		self.save()



""" 
-----------
SourceForge
-----------
"""

class SourceForgeProject(Project):
	"""
	SourceForge project class
	"""

	sourceforge_repo = models.CharField(max_length = 100, unique = True, blank = True, null = True)
	user_rating = models.DecimalField(max_digits = 4, decimal_places = 1, blank = True, null = True)
	downloads = models.IntegerField(blank = True, null = True)


	def collect_basic(self):
		"""
		Collects basic information about a sourceforge project (name, description, category, )
		"""

		pass


	def update_rating_downloads(self):
		"""
		Updates rating and download information about a project
		"""

		pass


	def update_activity_level(self):
		"""
		Updates activity level of project
		"""

		pass


	def update_rating(self):
		""" 
		Updates the project rating
		"""

		pass

	def update_project_info(self):
		""" 
		Method calling all the update functions 
		"""

		self.update_rating_downloads()
		self.update_activity_level()
		self.update_rating()
		self.save()



""" 
---------
BitBucket
---------
"""

class BitBucketProject(Project):
	"""
	BitBucket project class
	"""

	bitbucket_repo = models.CharField(max_length = 100, unique = True, blank = True, null = True)
	bitbucket_forks = models.IntegerField(blank = True, null = True)
	bitbucket_followers = models.IntegerField(blank = True, null = True)


	def collect_basic(self):
		"""
		Collects basic information about a sourceforge project (name, description, category, )
		"""

		self.bitbucket_repo = self.extract_bitbucket_repo()
		self.name = self.extract_name()
		self.category = self.predict_category()
		self.description = self.get_description()


	def update_forks_followers(self):
		"""
		Updates bitbucket forks and followers
		"""

		pass


	def update_activity_level(self):
		"""
		Updates activity level of project
		"""

		pass


	def update_rating(self):
		""" 
		Updates the project rating
		"""

		pass


	def update_project_info(self):
		""" 
		Method calling all the update functions 
		"""

		self.update_forks_followers()
		self.update_activity_level()
		self.update_rating()
		self.save()






class ModeratedProject(models.Model):
	""" 
	This class is used when a project is edited or created
	it must then be confirmed by a moderator through the 
	admin interface. After confirmation, this model is 
	converted to the complete Project model.
	"""
	
	name 				= models.CharField(max_length = 30)
	github_repo			= models.CharField(max_length = 100)
	category			= models.CharField(max_length = 100)
	comments			= models.TextField(blank = True)
	existing_project	= models.ForeignKey(Project, blank = True, null = True)

	def __unicode__(self):
		return self.name






