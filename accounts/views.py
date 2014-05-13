from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from accounts.models import UserProfile
from projects.models import Project
from accounts.forms import AccountSettingsForm

import logging
logger = logging.getLogger('log')

@login_required
def home(request):
	try:
		profile = UserProfile.objects.get(user = request.user)
	except:
		profile = UserProfile(user = request.user, receive_email = False)
		profile.save()
	profile.update_user_info() # NO UPDATE
	return render(request, 'account_details.html',{
		'profile': profile,
		})

@login_required
def settings(request):
	logger.info('enter SETTINGS')
	if request.POST:
		logger.info('enter POST')
		form = AccountSettingsForm(request.POST)
		if form.is_valid():
			logger.info('valid EMAIL')
			cd = form.cleaned_data


			current_email = request.user.email
			if current_email is not cd['email']:
				request.user.email = cd['email']
				request.user.save()


			user_profile = UserProfile.objects.get(user=request.user)
			user_profile.receive_email = cd['receive_email']
			logger.info(cd['receive_email'])
			user_profile.save()
		else:
			logger.info(form.errors)
		return redirect('accounts.views.home')

	else:
		form = AccountSettingsForm()
		form.initial['email'] = request.user.email
		return render(request, 'account_settings.html',{
			'form': form,
			})

def logout(request):
	logout_user(request)
	return redirect('categories.views.by_group')







