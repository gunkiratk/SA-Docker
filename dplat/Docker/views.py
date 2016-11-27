from django.shortcuts import render
from models import Name_pass,Container
def home_page(request):
	return render(request,"register.html",{})
def register(request):
	print "register"
	if(request.method=='POST'):
		name=request.POST['name']
		password=request.POST['password']
	return render(request,"utility.html",{'username':name})	
# Create your views here.
