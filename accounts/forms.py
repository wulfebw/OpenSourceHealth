from django import forms

class AccountSettingsForm(forms.Form):
	email = forms.EmailField(max_length=100)
	receive_email = forms.BooleanField(required=False)
	receive_email.widget.attrs['class'] = ''
