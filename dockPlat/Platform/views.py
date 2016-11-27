from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Container
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from docker import Client
# Create your views here.

cli = Client(base_url='unix://var/run/docker.sock')
def login(request):
	error=None
	if request.method == 'POST' :
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)

		if user is not None:
			if user.is_active :
				login (request, user)
				return redirect('dashboard')
			else :
				error = "Your account in not active. Talk to the owner of the site."

		else:
			error = "Invalid Credentials"

	context = {'error' : error }

	return render(request, 'login.html', context)


@login_required
def dashboard(request):
	current_user = User.objects.get(username_iexact=request.user)
	return request(request, 'home.html', {'user':current_user.first_name})

@login_required
def view_containers(request):
	current_user = User.objects.get(username_iexact=request.user)
	current_containers_list = current_user.conatiner_set.all()
	all_list = []
	exited_list = []
	running_list = []
	for i in current_containers_list :
		name = i.c_name
		all_list.append(cli.conatiners(all=True))
		exited_list.append(cli.conatiners(filters={'name'=name, 'status'='exited'}))
		running_list.append(cli.containers(filters={'name'=name, 'status'='running'}))

	#list verbose
	verbose_all_list = []
	verbose_exited_list = []
	verbose_running_list = []
	for i in all_list:
		disp_dict = {}
		disp_dict['Name'] = i['Names'][0]
		disp_dict['Status'] = i['Status']
		disp_dict['Command'] = i['Command']
		disp_dict['Ports'] = i['Ports']
		disp_dict['Image'] = i['Images']
		verbose_all_list.append(disp_dict)

	
	for i in exited_list:
		disp_dict = {}
		disp_dict['Name'] = i['Names'][0]
		disp_dict['Status'] = i['Status']
		disp_dict['Command'] = i['Command']
		disp_dict['Ports'] = i['Ports']
		disp_dict['Image'] = i['Images']
		verbose_exited_list.append(disp_dict)

	for i in running_list:
		disp_dict = {}
		disp_dict['Name'] = i['Names'][0]
		disp_dict['Status'] = i['Status']
		disp_dict['Command'] = i['Command']
		disp_dict['Ports'] = i['Ports']
		disp_dict['Image'] = i['Images']
		verbose_running_list.append(disp_dict)

	context = {'user':current_user.first_name, 'all':verbose_all_list, 'exited':verbose_exited_list, 'running':verbose_running_list}
	return render(request, 'home.html', context)


def register_user(request):
	error = None
	if request.method == 'POST' :

		name = request.POST['name'].split(" ")
		first_name = name[0]

		username, email, password = request.POST['username'], request.POST['email'] ,request.POST['password']

		existing = User.obejcts.filter(username_iexact=username)
		if(exisiting.exists()) :
			error = ("This username already exists!")
		else :
			new_user = User.objects.create_user(username, email, password)
			new_user.is_active = True
			new_user.first_name = first_name
			if len(name) == 2 : 
				last_name = name[1]
				new_user.last_name = last_name
			new_user.save()
			return redirect('login')
	return render(request, "signup,html", {'error':error})

@login_required
def logout_user(request):
	logout(request)
	return redirect("login")


@login_required
def run_container(request):
	current_user = User.objects.get(username_iexact=request.user)
	if request.method == 'POST' :
		container_name = request.POST['name']
		image_name = request.POST['image']
		command = request.POST['command']

		container = None
		if(command) :
			container = cli.creater_container(image=image_name, command=command, name=container_name)
		else:
			container = cli.creater_container(image=image_name, name=container_name)
		cli.start(costainer=container.get('Id'))
		response = cli.containers(filters=)
		c = Container(c_name=container_name, image_id=image_id)
		c.user = current_user
		c.save()
		return redirect("dashboard")




