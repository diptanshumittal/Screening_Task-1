from django.shortcuts import render , redirect
from django.http import HttpResponse
from calc.models import Rooms
from calc.models import Customer
from calc.models import Bookings
from calc.models import Manager
from django.http import HttpResponseRedirect
from datetime import datetime , timedelta
from django.contrib import messages
import re 
# Create your views here.




regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
auth = False 
m_auth = False
auth_user = [] 
rooms = []
bookings =[]

st = 0 
et = 0 

def logout(request):
	global auth
	auth = False
	global auth_user
	auth_user = []
	global m_auth
	m_auth = False
	return HttpResponseRedirect('/')

def viewbookings(request):
	if auth and m_auth :
		bkgs = Bookings.objects.all()
		li = []
		for bkg in bkgs:
			if(bkg.mid==auth_user.id):
				li.append(bkg)
		return render(request,'viewbookings.html' , {'bookings': li}); 
	else:
		return HttpResponseRedirect('/signinuser')


def changeslots(request):
	global rooms
	if(request.method=='POST'):
		t = request.POST['value']
		index = int(request.POST['room']) - 1
		room = rooms[index]
		if(t=="delete"):
			Rooms.objects.get(id = room.id).delete()
		else :
			st = int(request.POST['st'])
			et = int(request.POST['et'])
			d = datetime.strptime(request.POST['d'] , '%m-%d-%Y').date()
			ad = int(request.POST['ad'])
			ad = d - timedelta(days = ad)
			number = room.rn
			Rooms.objects.get(id = room.id).delete()
			room = Rooms( mid = auth_user.id  , startTime = st , endTime = et , rn = number , date = d , addate = ad , status = False)
			room.save()
		return HttpResponseRedirect('/')
	else:
		Ro = Rooms.objects.all()
		
		rooms = []
		for room in Ro :
			if(auth_user.id==room.mid):
				rooms.append(room)
		return render(request,'changeslots.html', {'rooms':rooms })





def addroom(request):
	global auth 
	if request.method=='POST':
		number = request.POST['number']
		st = int(request.POST['st'])
		et = int(request.POST['et'])
		d = datetime.strptime(request.POST['d'] , '%m-%d-%Y').date()
		a = int(request.POST['ad'])
		upd = datetime.strptime(request.POST['upd'] , '%m-%d-%Y').date()
		while(d<=upd):
			ad = d - timedelta(days = a)
			print(ad)
			print(auth_user.id)
			print(st)
			room = Rooms( mid = auth_user.id  , startTime = st , endTime = et , rn = number , date = d , addate = ad , status = False)
			room.save()
			d = d + timedelta(days=1)
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
	else:
		if(auth==True and m_auth==False):
			return render(request,'bookroom.html' , {'rooms':rooms , 'rsize' : range(len(rooms))});

def deletebookings(request):
	global bookings
	if auth and not m_auth :
		if(request.method=='POST'):
			index = int(request.POST['bid']) -1 
			print(index)
			booking = bookings[index]
			troom = Rooms.objects.get(id = booking.rid)
			roomlist = []
			rooms = Rooms.objects.all()
			for room in rooms:
				if(room.rn==troom.rn and room.mid==troom.mid and room.date==troom.date):
					roomlist.append(room)
			flag=0
			temp = []
			et = troom.endTime
			st = troom.startTime
			for room in roomlist:
				print("here")
				if(room.status==False):
					if(room.startTime==et):
						if(flag==0):
							room.startTime = st 
							room.save(update_fields = ['startTime'])
							Rooms.objects.get(id=troom.id).delete()
							flag=1
							temp = room 
						elif flag==1:
							temp.endTime = room.endTime 
							temp.save(update_fields = ['endTime'])
							Rooms.objects.get(id=room.id).delete()
							flag=2
					elif(room.endTime==st ):
						if flag ==0:
							room.endTime = et 
							room.save(update_fields = ['endTime'])
							Rooms.objects.get(id=troom.id).delete()
							flag=1 
							temp=room
						elif flag==1:
							temp.startTime = room.startTime 
							temp.save(update_fields = ['startTime'])
							Rooms.objects.get(id=room.id).delete()
							flag=2
			if(flag==0):
				troom.status = False
				troom.save(update_fields = ['status'])
			print(flag)
			Bookings.objects.get(id=booking.id).delete()
			return HttpResponseRedirect('/')
		else:
			bookings = []
			al = Bookings.objects.all()
			for ty in al :
				if(ty.cid == auth_user.id):
					bookings.append(ty)
			return render(request , 'bookings.html' , {'bookings':bookings , 'delete':True})
	else:
		return HttpResponseRedirect('/signinuser')

def bookings(request):
	global bookings
	bookings = []
	al = Bookings.objects.all()
	for ty in al :
		if(ty.cid == auth_user.id):
			bookings.append(ty)
	return render(request , 'bookings.html' , {'bookings':bookings , 'delete':False})

def bookroom1(request):
	if auth and not m_auth :
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
			return render(request,'bookroom.html' , {'rooms':rooms , 'rsize' : range(len(rooms))});
	else:
		return HttpResponseRedirect('/signinuser')
	
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
	global regex
	if request.method == 'POST':

		customers = Customer.objects.all()
		loginid = request.POST['loginid']
		if(len(loginid)<1):
			messages.info(request,'Loginid cant be empty')
			return HttpResponseRedirect('/signupuser')
		for customer in customers:
			if(customer.loginid == loginid):
				messages.info(request,'Loginid already taken')
				return HttpResponseRedirect('/signupuser')

		password = request.POST['password']
		if(len(password)<8):
			messages.info(request,'Password too weak')
			return HttpResponseRedirect('/signupuser')

		name = request.POST['name']
		if(len(name)<1):
			messages.info(request,'Name cant be empty')
			return HttpResponseRedirect('/signupuser')
		email = request.POST['email']
		if(len(email)<1):
			messages.info(request,'Email cant be empty')
			return HttpResponseRedirect('/signupuser')
		elif(not re.search(regex,email)): 
			messages.info(request,'Email invalid')
			return HttpResponseRedirect('/signupuser')
		customer = Customer(loginid = loginid , name = name , password = password , email = email)
		customer.save()
		print(customer.id)
		print("user created")
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