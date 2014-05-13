from django.shortcuts import render, get_object_or_404
from categories.models import Category, Group
from django.http import HttpResponseRedirect
from projects.models import Project, ModeratedProject
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from projects.forms	import ModeratedProjectForm
from django.core.urlresolvers import reverse

import datetime
import requests

import logging
logger = logging.getLogger('log')

def project_detail(request, project_name, like = 0):
	project = get_object_or_404(Project, name = project_name)
	project.update_project_info()		
	now = datetime.datetime.now()

	if request.user.is_authenticated():
		user_signed_in = True
	else:
		user_signed_in = False

	if like and user_signed_in:
		profile = UserProfile.objects.get(user = request.user)
		if profile:
			profile.favorite_projects.add(project)
			profile.save()
		like = True
	else:
		if user_signed_in:
			profile = UserProfile.objects.get(user = request.user)
		else:
			profile = None
		if profile and profile.favorite_projects.filter(name = project_name).exists():
			like = True
	return render(request, 'project_detail.html', {
		'project': project,
		'cur_date': now,
		'like': like,
		})

def projects_by_name(request):
	projects = Project.objects.all().extra(select={'name_lower': 'lower(name)'}).order_by('name_lower')
	return render(request, 'projects_by_name.html', {
		'projects': projects,
		})

@login_required
def edit_project(request, project_name):
	try:
		existing_project = Project.objects.get(name = project_name)
	except:
		existing_project = None

	if existing_project is None:
		is_existing_project = False
	else:
		is_existing_project = True

	if request.POST:
		form = ModeratedProjectForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			logger.info('cd: {0}\n'.format(cd))
			logger.info(cd['github_repo'])

			# r = requests.get('https://api.github.com/repos/{0}'.format(github_repo = cd['github_repo']))
			# if not r.ok:
			# 	errors.append("invalid github repo")
			# 	return render(request, 'edit_project.html', {
			# 		'form': form,
			# 		'errors': errors,
			# 		})
			new_mod_project = ModeratedProject(
				name = cd['name'],
				github_repo = cd['github_repo'],
				category = cd['category'],
				comments = cd['comments'],
				)
			if is_existing_project:
				try:
					existing_project = Project.objects.get(name = project_name)
					new_mod_project.existing_project = existing_project
				except Exception:
					pass
			new_mod_project.save()
		if is_existing_project:
			return HttpResponseRedirect(reverse('projects.views.project_detail', args=(project_name,)))
		else: 
			return HttpResponseRedirect(reverse('projects.views.projects_by_name'))
				
	else:
		form = ModeratedProjectForm()
		if is_existing_project:
			existing_project = get_object_or_404(Project, name = project_name)
			form.initial['name'] = existing_project.name
			form.initial['category'] = existing_project.category
			form.initial['github_repo'] = existing_project.github_repo
	return render(request, 'edit_project.html', {
		'form': form,
		})













