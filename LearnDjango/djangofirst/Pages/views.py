from django.http import HttpResponse 
from django.shortcuts import render

# Create your views here.
#just a simple python function
#so far nothing to do with django
def upload_view(request, *args, **kwargs):
	return render(request, "upload.html", {} ) #String of html code

def loginToUpload_view(request, *args, **kwargs):
	return render(request, "loginToUpload.html", {} ) #String of html code

def home_view(request, *args, **kwargs):
	return HttpResponse("<hi>Hello to contact view</h1>") #String of html code