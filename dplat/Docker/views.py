from django.shortcuts import render
from models import Name_pass,Container
# from docker import Client
def home_page(request):
	return render(request,"register.html",{})
def register(request):
	if(request.method=='POST'):
		name=request.POST['name']
		password=request.POST['password']
		Username=request.POST['username']
	return render(request,"utility.html",{'username':Username})
def run(request):
	return render(request,"run.html",{})
def view(request):
	return render(request,"view.html",{})
# Create your views here.
