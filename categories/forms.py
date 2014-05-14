from django import forms
from projects.models import ModeratedCategory

class ModeratedCategoryForm(forms.Form):
	name = forms.CharField(max_length=30, required=False)
	group = forms.CharField(max_length=30, required=False)

