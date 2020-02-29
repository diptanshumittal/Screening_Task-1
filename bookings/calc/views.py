from django.shortcuts import render , redirect
from django.http import HttpResponse
from calc.models import Rooms
from calc.models import User
from calc.models import Admin
from django.http import HttpResponseRedirect
# Create your views here.


auth = False 

auth_user = [] 



def home(request):
	print(auth)
	return render(request,'home.html' , {'data' : auth, 'user' : auth_user});

def add(request):
	val1 = int(request.POST["num1"])
	val2 = int(request.POST["num2"])
	res = val1+val2
	return render(request,'result.html', {'result': res});

def login(request):
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
		return HttpResponseRedirect('/accounts/login')
	else:
		return render(request , 'login.html')
def register(request):
	if request.method == 'POST':
		loginid = request.POST['loginid']
		password = request.POST['password']
		name = request.POST['name']
		email = request.POST['email']
		contact_number = int(request.POST['contact_number'])
		user = User(loginid = loginid , name = name , password = password , email = email , contact_number = contact_number)
		user.save();
		print("user created")
		return HttpResponseRedirect('/')
	else:
		return render(request , 'register.html')