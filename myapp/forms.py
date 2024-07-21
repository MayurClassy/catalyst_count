from django import forms
from django import forms
from django.contrib.auth.models import User

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()


class QueryBuilderForm(forms.Form):
    name = forms.CharField(required=False)
    domain = forms.CharField(required=False)
    year_founded = forms.IntegerField(required=False)
    industry = forms.CharField(required=False)
    size_range = forms.CharField(required=False)
    locality = forms.CharField(required=False)
    country = forms.CharField(required=False)
    linkedin_url = forms.URLField(required=False)
    current_employee_estimate = forms.IntegerField(required=False)
    total_employee_estimate = forms.IntegerField(required=False)



class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

