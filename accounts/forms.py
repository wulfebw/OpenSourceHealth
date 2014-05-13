from django import forms

class AccountSettingsForm(forms.Form):
	email = forms.EmailField(max_length=100)
	receive_news = forms.BooleanField(required=False)
	receive_news.widget.attrs['class'] = ''
