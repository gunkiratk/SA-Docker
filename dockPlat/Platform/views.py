from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Container
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from docker import Client
# Create your views here.

cli = Client(base_url='unix://var/run/docker.sock')
def login_user(request):
	error=None
	print ("login page")
	if request.method == 'POST' :
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)

		if user is not None:
			if user.is_active :
				login(request, user)
				return redirect('dashboard')
			else :
				error = "Your account in not active. Talk to the owner of the site."

		else:
			error = "Invalid Credentials"

	context = {'error' : error }

	return render(request, 'login.html', context)


@login_required
def dashboard(request):
	current_user = User.objects.get(username__iexact=request.user)
	return render(request, 'home.html', {'user':current_user.first_name})

@login_required
def view_containers(request):
	current_user = User.objects.get(username__iexact=request.user)
	return render(request, 'view.html', {'user':current_user.first_name})

@login_required
def view_all(request):
	current_user = User.objects.get(username__iexact=request.user)
	current_containers_list = current_user.container_set.all()
	all_list = []
	for i in current_containers_list :
		name = i.c_name
		all_list.append(cli.containers(all=True, filters={'name':name}))

	#list verbose
	verbose_all_list = []
	for i in all_list:
		disp_dict = {}
		disp_dict['Name'] = i[0]['Names'][0]
		disp_dict['Status'] = i[0]['Status']
		disp_dict['Command'] = i[0]['Command']
		disp_dict['Ports'] = i[0]['Ports']
		disp_dict['Image'] = i[0]['Image']
		verbose_all_list.append(disp_dict)

	context = {'user':current_user.first_name, 'all':verbose_all_list}
	return render(request, 'all.html', context)

@login_required
def view_exited(request):
	current_user = User.objects.get(username__iexact=request.user)
	current_containers_list = current_user.container_set.all()
	exited_list = []
	verbose_exited_list = []

	for i in current_containers_list :
		name = i.c_name
		exited_list.append(cli.containers(filters={'name':name, 'status':'exited'}))

	for i in exited_list:
		if i :
			disp_dict = {}
			disp_dict['Name'] = i[0]['Names'][0]
			disp_dict['Status'] = i[0]['Status']
			disp_dict['Command'] = i[0]['Command']
			disp_dict['Ports'] = i[0]['Ports']
			disp_dict['Image'] = i[0]['Image']
			verbose_exited_list.append(disp_dict)

	context = {'user':current_user.first_name, 'all':verbose_exited_list}

	return render(request, 'exited.html', context)

@login_required
def view_running(request):
	current_user = User.objects.get(username__iexact=request.user)
	current_containers_list = current_user.container_set.all()
	running_list = []
	verbose_running_list = []

	for i in current_containers_list :
		name = i.c_name
		running_list.append(cli.containers(filters={'name':name, 'status':'running'}))

	for i in running_list:
		if i :
			disp_dict = {}
			disp_dict['Name'] = i[0]['Names'][0]
			disp_dict['Status'] = i[0]['Status']
			disp_dict['Command'] = i[0]['Command']
			disp_dict['Ports'] = i[0]['Ports']
			disp_dict['Image'] = i[0]['Image']
			verbose_running_list.append(disp_dict)

	context = {'user':current_user.first_name, 'all':verbose_running_list}

	return render(request, 'running.html', context)

@login_required
def view_paused(request):
	current_user = User.objects.get(username__iexact=request.user)
	current_containers_list = current_user.container_set.all()
	paused_list = []
	verbose_paused_list = []

	for i in current_containers_list :
		name = i.c_name
		paused_list.append(cli.containers(filters={'name':name, 'status':'paused'}))

	for i in paused_list:
		if i :
			disp_dict = {}
			disp_dict['Name'] = i[0]['Names'][0]
			disp_dict['Status'] = i[0]['Status']
			disp_dict['Command'] = i[0]['Command']
			disp_dict['Ports'] = i[0]['Ports']
			disp_dict['Image'] = i[0]['Image']
			verbose_paused_list.append(disp_dict)

	context = {'user':current_user.first_name, 'all':verbose_paused_list}

	return render(request, 'paused.html', context)

def register_user(request):
	error = None
	print ("views.register user")
	if request.method == 'POST' :
		print ("Post request in register")
		name = request.POST['name'].split(" ")
		first_name = name[0]

		username, email, password = request.POST['username'], request.POST['email'] ,request.POST['password']

		existing = User.objects.filter(username__iexact=username)
		if(existing.exists()) :
			error = ("This username already exists!")
			return render(request, "register.html", {'error' : error})
		else :
			new_user = User.objects.create_user(username, email, password)
			new_user.is_active = True
			new_user.first_name = first_name
			if len(name) == 2 : 
				last_name = name[1]
				new_user.last_name = last_name
			new_user.save()
			return redirect('login')
	return render(request, "register.html", {'error':error})

@login_required
def logout_user(request):
	logout(request)
	return redirect('login')


@login_required
def run_container(request):
	current_user = User.objects.get(username__iexact=request.user)
	if request.method == 'POST' :
		print (request.POST)
		container_name = request.POST['name']
		image_name = request.POST['image']
		command = request.POST['command']
		detach = request.POST['detatched']
		if(detach == 1):
			detach = True
		else:
			detach = False
		container = None
		error = None
		# try:
		if(command) :
			container = cli.create_container(image=image_name, command=command, name=container_name, detach=detach, ports=[8080], host_config = cli.create_host_config(port_bindings={8080: 4567}))
		else:
			container = cli.create_container(image=image_name, name=container_name, detach=detach, ports=[8080], host_config = cli.create_host_config(port_bindings={8080: 4567}))
		cli.start(container=container.get('Id'))
		obj = cli.containers(filters={'name':container_name}, all=True)
		image_id = obj[0]['ImageID']
		c = Container(c_name=container_name, image_id=image_id)
		c.author = current_user
		c.save()
		return redirect("dashboard")
		# except:
			# error = "This container name already exists"
			# return render(request, 'run.html', {'error':error})

	return render(request, 'run.html', {'user':current_user.first_name})


@login_required	
def manage_container(request):
	current_user = User.objects.get(username__iexact=request.user)
	current_containers_list = current_user.container_set.all()	
	context = {'status':None, 'conList' : current_containers_list}
	if request.method == 'POST':
		container_name = request.POST['conSel']
		getCon = cli.containers(filters={'name':container_name}, all=True)
		if(getCon):
			status = getCon[0]['Status']
			con_Id = getCon[0]['Id']
		if('start' in request.POST) : 
			cli.start(container=con_Id)
			return redirect("all")
		elif('stop' in request.POST) :
			cli.stop(container_name)
			return redirect("all")
		elif('pause' in request.POST) : 
			cli.pause(container_name)
			return redirect("all")
		elif('unpause' in request.POST) :
			cli.unpause(container_name)
			return redirect("all")
		elif('delete' in request.POST):
			cli.remove_container(container_name)
			con = Container.objects.get(c_name=container_name)
			con.delete()
			return redirect("all")
		elif('status' in request.POST):
			context['status'] = status
	return render(request, 'manage.html', context)




