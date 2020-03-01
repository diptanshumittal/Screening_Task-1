from django.shortcuts import render , redirect
from django.http import HttpResponse
from calc.models import Rooms
from calc.models import User
from calc.models import Manager
from django.http import HttpResponseRedirect
# Create your views here.


auth = False 
manager = False
auth_user = [] 
rooms = []
def logout(request):
	global auth
	auth = False
	global auth_user
	auth_user = []
	return HttpResponseRedirect('/')


def addroom(request):
	if request.method=='POST':
		number = request.POST['number']
		userid = request.POST['userid']
		managerid = request.POST['managerid']
		slot = request.POST['slot']
		return HttpResponseRedirect('addroom')
	else:
		return render(request,'addroom.html');

def home(request):
	if request.method=='POST':
		val1 = int(request.POST["num1"])
		val2 = int(request.POST["num2"])


	print(auth)
	return render(request,'home.html' , {'data' : auth, 'user' : auth_user , 'manager':manager , 'rooms':rooms});

def add(request):
	val1 = int(request.POST["num1"])
	val2 = int(request.POST["num2"])
	res = val1+val2
	return render(request,'result.html', {'result': res});

def signinmanager(request):
	if request.method == 'POST':
		loginid = request.POST['loginid']
		password = request.POST['password']
		users = Manager.objects.all()
		for user in users:
			if(user.loginid==loginid and user.password == password):
				global auth
				global manager 
				manager= True
				auth = True
				global auth_user
				auth_user = user
				print("verified "+user.name)
				return HttpResponseRedirect('/')
		return HttpResponseRedirect('signinmanager')
	else:
		return render(request , 'signinmanager.html')

def signinuser(request):
	if request.method == 'POST':
		loginid = request.POST['loginid']
		password = request.POST['password']
		users = User.objects.all()
		for user in users:
			if(user.loginid==loginid and user.password == password):
				global auth 
				auth = True
				global auth_user
				auth_user = user
				print("verified")
				return HttpResponseRedirect('/')
		return HttpResponseRedirect('/signinuser')
	else:
		return render(request , 'signinuser.html')


def signin(request):
	return render(request , 'signin.html')



def signup(request):
	return render(request , 'signup.html')



def signupuser(request):
	if request.method == 'POST':
		loginid = request.POST['loginid']
		password = request.POST['password']
		name = request.POST['name']
		email = request.POST['email']
		contact_number = int(request.POST['contact_number'])
		managers = User.objects.all()
		flag=0
		for manager in managers:
			if(manager.loginid == loginid):
				flag=1
		if(flag==0):
			user = User(loginid = loginid , name = name , password = password , email = email , contact_number = contact_number)
			user.save();
			print("user created")
		else:
			return HttpResponseRedirect('/signupuser')
		return HttpResponseRedirect('/')
	else:
		return render(request , 'signupuser.html')


def signupmanager(request):
	if request.method == 'POST':
		loginid = request.POST['loginid']
		password = request.POST['password']
		name = request.POST['name']
		email = request.POST['email']
		contact_number = int(request.POST['contact_number'])
		managers = Manager.objects.all()
		flag=0
		for manager in managers:
			if(manager.loginid == loginid):
				flag=1
		if(flag==0):
			user = Manager(loginid = loginid , name = name , password = password , email = email , contact_number = contact_number)
			user.save();
			print("Manager created")
		else:
			return HttpResponseRedirect('/signupmanager')
		return HttpResponseRedirect('/')
	else:
		return render(request , 'signupmanager.html')