from django import forms
from projects.models import ModeratedProject

class ModeratedProjectForm(forms.ModelForm):
	class Meta:
		model = ModeratedProject
		exclude = ['existing_project']

