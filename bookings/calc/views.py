from django.shortcuts import render , redirect
from django.http import HttpResponse
from calc.models import Rooms
from calc.models import Customer
from calc.models import Bookings
from calc.models import Manager
from django.http import HttpResponseRedirect
from datetime import datetime , timedelta
# Create your views here.


auth = False 
m_auth = False
auth_user = [] 
rooms = []

st = 0 
et = 0 

def logout(request):
	global auth
	auth = False
	global auth_user
	auth_user = []
	return HttpResponseRedirect('/')


def addroom(request):
	global auth 
	if request.method=='POST':
		number = request.POST['number']
		st = int(request.POST['st'])
		et = int(request.POST['et'])
		d = datetime.strptime(request.POST['d'] , '%m-%d-%Y').date()
		ad = int(request.POST['ad'])
		ad = d - timedelta(days = ad)
		print(ad)
		print(auth_user.id)
		print(st)
		room = Rooms( mid = auth_user.id  , startTime = st , endTime = et , rn = number , date = d , addate = ad , status = False)
		room.save()
		return HttpResponseRedirect('addroom')
	else:
		if(auth == False or m_auth==False):
			return HttpResponseRedirect('signinmanager')
		return render(request,'addroom.html');

def bookroom(request):
	if request.method=='POST':
		index = int(request.POST['room']) -1 
		print(index)
		room = rooms[index]
		if(room.startTime==st):
			if(room.endTime==et):
				temp = Rooms.objects.get(id=room.id)
				temp.status = True
				temp.save(update_fields = ['status'])
			else:
				temp = Rooms.objects.get(id=room.id)
				temp.status = True
				p = temp.endTime
				temp.endTime = et
				temp.save(update_fields = ['status'])
				temp.save(update_fields = ['endTime'])
				ty = Rooms( mid = temp.mid  , startTime = et , endTime = p , rn = temp.rn , date = temp.date , addate = temp.addate , status = False)
				ty.save()
		elif (room.endTime == et):
			temp = Rooms.objects.get(id=room.id)
			temp.status = True
			p = temp.startTime
			temp.startTime = st
			temp.save(update_fields = ['status'])
			temp.save(update_fields = ['startTime'])
			ty = Rooms( mid = temp.mid  , startTime = p , endTime = st , rn = temp.rn , date = temp.date , addate = temp.addate , status = False)
			ty.save()
		else:
			temp = Rooms.objects.get(id=room.id)
			temp.status = True
			pe = temp.endTime
			p = temp.startTime
			temp.startTime = st
			temp.endTime = et 
			temp.save(update_fields = ['status'])
			temp.save(update_fields = ['startTime'])
			temp.save(update_fields = ['endTime'])
			ty = Rooms( mid = temp.mid  , startTime = p , endTime = st , rn = temp.rn , date = temp.date , addate = temp.addate , status = False)
			ty.save()
			ty = Rooms( mid = temp.mid  , startTime = et , endTime = pe , rn = temp.rn , date = temp.date , addate = temp.addate , status = False)
			ty.save()

		book = Bookings(rid = room.id , cid = auth_user.id , mid = room.mid)
		book.save()
		print(book)
		print(room)
		return HttpResponseRedirect('/')

def home(request):
	global rooms
	rooms=[]
	if request.method=='POST':
		d = datetime.strptime(request.POST['d'] , '%m-%d-%Y').date()
		global st 
		global et
		st = int(request.POST['st'])
		et = int(request.POST['et'])
		temp = Rooms.objects.all()
		for t in temp:
			if(t.status==False and t.date == d and t.addate<d):
				print("here")
				if(t.startTime<=st and t.endTime>=et):
					print("here")
					rooms.append(t)
		return render(request,'home.html' , {'auth' : auth, 'user' : auth_user , 'manager':m_auth , 'rooms':rooms , 'rsize' : range(len(rooms))});
	else:
		return render(request,'home.html' , {'auth' : auth, 'user' : auth_user , 'manager':m_auth , 'rooms':rooms , 'rsize' : range(len(rooms))});


def signinmanager(request):
	if request.method == 'POST':
		loginid = request.POST['loginid']
		password = request.POST['password']
		users = Manager.objects.all()
		for user in users:
			if(user.loginid==loginid and user.password == password):
				global auth
				global m_auth 
				m_auth= True
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
		users = Customer.objects.all()
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
		customers = Customer.objects.all()
		flag=0
		for customer in customers:
			if(customer.loginid == loginid):
				flag=1
		if(flag==0):
			customer = Customer(loginid = loginid , name = name , password = password , email = email)
			customer.save()
			print(customer.id)
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
		managers = Manager.objects.all()
		flag=0
		for manager in managers:
			if(manager.loginid == loginid):
				flag=1
		if(flag==0):
			user = Manager(loginid = loginid , name = name , password = password , email = email)
			user.save();
			print(user.id)
			print("Manager created")
		else:
			return HttpResponseRedirect('/signupmanager')
		return HttpResponseRedirect('/')
	else:
		return render(request , 'signupmanager.html')