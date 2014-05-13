from django.shortcuts import render, get_object_or_404
from categories.models import Category, Group
from projects.models import Project
from accounts.models import UserProfile

import logging
logger = logging.getLogger('log')

def by_group(request):
	categories = Category.objects.all().order_by('group','name')
	for c in categories:
		c.projects = Project.objects.filter(category = c)
	return render(request, 'categories_by_group.html', {
		'categories': categories,
		})

def by_name(request):
	categories = Category.objects.all().order_by('name')
	for c in categories:
		c.projects = Project.objects.filter(category = c).order_by('rating').reverse()
	return render(request, 'categories_by_name.html', {'categories': categories})

def category_detail(request, category_name):
	category = get_object_or_404(Category, name = category_name)
	projects = Project.objects.filter(category = category).order_by('rating').reverse()
	favorite_list = []
	try:
		user_profile = UserProfile.objects.get(user = request.user)
	except:
		user_profile = None

	if user_profile is not None:
		for proj in user_profile.favorite_projects.all():
			favorite_list.append(proj)
	
	# convert to a scheduled job run on the server
	# # for p in projects:
	# # 	p.update_project_info()
	return render(request, 'category_detail.html', {
		'category': category,
		'projects': projects,
		'favorites': favorite_list,
		})


		


