from django.db import models
from categories.models import *
from django.contrib.auth.models import User
import requests
import json
import datetime


NUM_COMMITS_USED_FOR_ACTIVITY_LEVEL = 15


class Project(models.Model):
	"""
	Abstract base class for the other project types
	"""

	# The website url is the only piece of information required originally
	# e.g., 
	#
	#	https://github.com/wulfebw/OpenSourceHealth
	#	https://bitbucket.org/pypy/pypy

	website_url = models.URLField(max_length = 100)

	name = models.CharField(max_length = 30, unique = True)
	category = models.ForeignKey(Category, blank = True, null = True)
	rating = models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, null = True)
	description = models.TextField(blank = True, null = True)	
	activity_level = models.IntegerField(blank = True, null = True)

	def __unicode__(self):
		return self.name


	def first_letter(self):
		""" 
		Method used to group projects in the template using 'regroup' 
		"""

		return self.name[0].upper() or ''


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

		This is called only when the project is initially suggested by a user
		"""

		self.github_repo = self.extract_github_repo()
		self.name = self.extract_name()
		self.category = self.predict_category()
		self.description = self.get_description()
		self.save()


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


	def extract_bitbucket_repo(self):
		"""
		Extracts the bitbucket repo name by finding the ".org" in the name and assuming the next two words seperated by forward slashes are the repo identifying values
		"""

		try:
			start = self.website_url.find('.org') + 5
			return '/'.join(self.website_url[start:].split('/')[:2])
		except Exception as e:
			logger.info(e)


	def collect_basic(self):
		"""
		Collects basic information about a sourceforge project (name, description, category)

		This is called only when the project is initially suggested by a user
		"""

		self.bitbucket_repo = self.extract_bitbucket_repo()

		try:
			r = requests.get('https://bitbucket.org/api/1.0/repositories/{0}'.format(self.bitbucket_repo))
		except Exception as e:
			logger.info(e)

		if r.ok:
			data = r.json()
			self.name = data[u'name']
			self.description = data[u'description']
		self.save()




	def update_forks_followers(self, data):
		"""
		Updates bitbucket forks and followers
		"""

		self.bitbucket_forks = data[u'forks_count']
		self.bitbucket_followers = data[u'followers_count']


	def get_avg_time_of_last_n_commits(self, data, n):
		"""
		Determines the average time since the last n commits (in days)
		"""

		commit_date_list = []
		today = datetime.datetime.now()
		changesets = data[u'changesets']
		max_index = min(n,len(data))

		for x in range(max_index):
			current_date_string = data[x][u'timestamp']
			try:
				year = current_date_string[:4]
				month = current_date_string[5:7]
				day = current_date_string[8:10]
				commit_date_list.append(datetime.datetime(year, month, day))
			except Exception as e:
				logger.info(e)

		total_difference_in_days = 0
		for date in commit_date_list:
			total_difference_in_days += (today - date).days

		return total_difference_in_days / float(max_index)


	def update_activity_level(self):
		"""
		Updates activity level of project
		"""

		try:
			r = requests.get('https://bitbucket.org/api/1.0/repositories/{0}/changesets/'.format(self.bitbucket_repo))
			if r.ok:
				data = r.json()
				avg_time_of_last_n_commits = get_avg_time_of_last_n_commits(data, NUM_COMMITS_USED_FOR_ACTIVITY_LEVEL)
		pass


	def update_rating(self, data):
		""" 
		Updates the project rating
		"""

		pass


	def update_project_info(self):
		""" 
		Method calling all the update functions 
		"""

		try:
			r = requests.get('https://bitbucket.org/api/1.0/repositories/{0}'.format(self.bitbucket_repo))
		except Exception as e:
			logger.info(e)

		if r.ok:
			data = r.json()
			self.update_forks_followers(data)
			self.update_activity_level()
			self.update_rating(data)
			self.save()



""" 
----------------
ModeratedProject
----------------
"""

class ModeratedProject(models.Model):
	""" 
	This class is used when a project is edited or created it must then be confirmed by a moderator
	through the admin interface. After confirmation, this model is converted to the complete 
	Project model.
	"""

	name 				= models.CharField(max_length = 30)
	github_repo			= models.CharField(max_length = 100)
	category			= models.CharField(max_length = 100)
	comments			= models.TextField(blank = True)
	existing_project	= models.ForeignKey(Project, blank = True, null = True)

	def __unicode__(self):
		return self.name






