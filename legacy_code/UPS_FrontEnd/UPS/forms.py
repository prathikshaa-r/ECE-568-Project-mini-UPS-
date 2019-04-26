from django import forms

class PIDForm(forms.Form):
        pid = forms.IntegerField(label='Search By Package ID')
