from django import  forms
from .models import article


class articleForm(forms.ModelForm):
    title=forms.CharField()
    text=forms.CharField()
    class Meta:
        model=task
        fields=[
'title',
'text'

        ]
    def clean_title(self,*args,**kwargs):
        title=self.cleaned_data.get("title")
        if "CFE" in title:
            return title
        else:
            raise forms.ValidationError("error")