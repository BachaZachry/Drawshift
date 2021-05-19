from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def home_view(request,*args, **kwargs):
    myContext={

        "myText":"aaa",
        "key":369
    }
    return render(request,"home.html",myContext)
def contact_view(request,*args, **kwargs):
    return render(request,"contact.html",{})