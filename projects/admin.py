from django.contrib import admin
from projects.models import Project, ModeratedProject
from categories.models import Category
from django.contrib import messages
import requests


import logging
logger = logging.getLogger('log')


class ModeratedProjectAdmin(admin.ModelAdmin):
	fields = ('name', 'github_repo', 'category', 'comments', 'existing_project')
	list_display = ('name', 'github_repo', 'category', 'comments', 'existing_project')
	ordering = ['name']
	actions = ['allow_changes']

	def allow_changes(self, request, queryset):
		for proj in queryset:
			# (1) check if this project has a corresponding existing project
				# (1a) check for valid github and category name
			# (2a) if so, echo these details to that existing project
			# (2b) if not, create a new project 
			# (3) delete the moderated project if applicable
			# (4) return response


			# (1) check if this project has a corresponding existing project
			has_existing_project = proj.existing_project is not None
			# check if github repo exists
			r = requests.get('https://api.github.com/repos/{0}'.format(proj.github_repo))
			valid_github = r.ok
			# check if category exists. If it doesn't assign to None
			try:
				valid_category = Category.objects.get(name = proj.category)
			except:
				valid_category = None
		
			# (2a) if so, echo these details to the existing project
			if has_existing_project:
				if valid_github:
					proj.existing_project.name = proj.name
					proj.existing_project.github_repo = proj.github_repo
					proj.existing_project.category = proj.category
					proj.existing_project.update_project_info()
					proj.existing_project.save()

			# (2b) if not, create a new project
			else:
				# create the project if github exists
				if valid_github:
					new_project = Project(	name = proj.name,
											github_repo = proj.github_repo,
											category = valid_category,
										)
					new_project.update_project_info()
					new_project.save()


			# (3) delete the moderated project or report error on no github
			if valid_github:
				proj.delete()
			else:
				# invalid github, do nothing?
				pass

	allow_changes.short_description = "Enact the proposed changes selected below"

admin.site.register(Project)
admin.site.register(ModeratedProject, ModeratedProjectAdmin)
