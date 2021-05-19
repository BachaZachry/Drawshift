from django import forms
from .models import task
class taskForm(forms.ModelForm):
    class Meta:
        model=task
        fields=[
'title',
'description',
'member',

        ]
    def clean_title(self,*args,**kwargs):
        title=self.cleaned_data.get("title")
        if "CFE" in title:
            return title
        else:
            raise forms.ValidationError("error")

class RawtaskForm(forms.Form):
    title=forms.CharField()
    description=forms.CharField()
  