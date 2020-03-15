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
from calc.forms import CheckRoom
from calc.forms import Signup
from calc.forms import AddRoomForm
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
		bookings = []
		ongoing = [] 
		al = Bookings.objects.all()
		for ty in al :
			if(ty.mid == auth_user.id):
				room = Rooms.objects.get(id=ty.rid)
				if(room.date<=datetime.date(datetime.now())):
					bookings.append((ty,room))
				else:
					ongoing.append((ty,room))
		show1 = True
		show = True
		if(len(bookings)==0):
			show1 = False
		if(len(ongoing)==0):
			show=False
		if(show==False and show1==False):
			messages.info(request,'No bookings done ')
			form = CheckRoom
			return HttpResponseRedirect('/' , {'form', form})
		return render(request , 'viewbookings.html' , {'bookings':bookings , 'delete':True , 'show':show ,'show':show , 'ongoing' : ongoing })
	else:
		messages.info(request,'Login to view bookings')
		return HttpResponseRedirect('/signinmanager')

def changeslots(request):
	global rooms
	form = AddRoomForm
	if auth:
		if(request.method=='POST'):
			t = request.POST['value']
			index = int(request.POST['room']) - 1
			room = rooms[index]
			if(t=="delete"):
				Rooms.objects.get(id = room.id).delete()
			else :
				st = int(request.POST['st'])
				et = int(request.POST['et'])
				d = datetime.strptime(request.POST['d'] , '%Y-%m-%d').date()
				ad = int(request.POST['ad'])
				ad = d - timedelta(days = ad)
				number = room.rn
				Rooms.objects.get(id = room.id).delete()
				room = Rooms( mid = auth_user.id  , startTime = st , endTime = et , rn = number , date = d , addate = ad , status = False)
				room.save()
			form = CheckRoom
			return HttpResponseRedirect('/' , {'form', form})
		else:
			Ro = Rooms.objects.all()
			rooms = []
			for room in Ro :
				if(auth_user.id==room.mid):
					rooms.append(room)
			if(len(rooms)==0):
				return render(request,'changeslots.html' , {'show':False } )
			return render(request,'changeslots.html', {'rooms':rooms , 'show':True , 'form':form })
	else:
		messages.info(request,'Need to login as manager to change room slots')
		return HttpResponseRedirect('signinmanager')
		
def addroom(request):
	global auth 
	form = AddRoomForm
	if request.method=='POST':
		rn = int(request.POST['number'])
		ste = int(request.POST['st'])
		ete = int(request.POST['et'])
		d = datetime.strptime(request.POST['d'] , '%Y-%m-%d').date()
		if( d <  datetime.date(datetime.now()) ):
			messages.info(request,'Cannot add room in back date')
			return HttpResponseRedirect('addroom' , {'form':form })
		a = int(request.POST['ad'])
		upd = datetime.strptime(request.POST['upd'] , '%Y-%m-%d').date()
		while(d<=upd):
			st = ste
			et = ete
			ad = d - timedelta(days = a)
			alrooms = Rooms.objects.all()
			flag=0
			print(len(alrooms)) 
			trom = []
			for t in alrooms:
				print("here")
				if(t.status == False):
					print("level2")
					if( t.mid == auth_user.id):
						print("level3")
						if(t.date == d):
							print("level4")
							print(t.rn)
							print(rn)
							if(t.rn == rn ):
								print("level5")
								trom.append(t)
			print(len(trom))
			for t in trom:
				if(t.startTime<=st and t.endTime>=et):
					st = t.startTime
					et = t.endTime
					Rooms.objects.get(id=t.id).delete()
				elif(t.startTime<st and t.endTime >= st and t.endTime<=et):
					st = t.startTime
					Rooms.objects.get(id=t.id).delete()
				elif(t.endTime>=et and t.startTime>= st and t.startTime<=et ):
					et = t.endTime
					Rooms.objects.get(id=t.id).delete()
				elif(t.startTime>=st and t.startTime<=et and t.endTime>=st and t.endTime<=et):
					Rooms.objects.get(id=t.id).delete()
			room = Rooms( mid = auth_user.id  , startTime = st , endTime = et , rn = rn , date = d , addate = ad , status = False)
			room.save()
			d = d + timedelta(days=1)
		return HttpResponseRedirect('addroom' , {'form':form })
	else:
		if(auth == False or m_auth==False):
			messages.info(request,'Need to login as manager to add room slots')
			return HttpResponseRedirect('signinmanager')
		return render(request,'addroom.html' , {'form':form } )

def bookroom(request):
	global rooms
	form = CheckRoom
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
		form = CheckRoom
		return HttpResponseRedirect('/' , {'form', form})
	else:
		if(auth==True and m_auth==False):
			return render(request,'bookroom.html' , {'form':form})
		else:
			messages.info(request,'Login as user to book the room ')
			return HttpResponseRedirect('/signinuser')

def deletebookings(request):
	global bookings
	if auth :
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
			ongoing = [] 
			al = Bookings.objects.all()
			for ty in al :
				if(ty.cid == auth_user.id):
					room = Rooms.objects.get(id=ty.rid)
					if(room.date<=datetime.date(datetime.now())):
						bookings.append((ty,room))
					else:
						ongoing.append((ty,room))
			show1 = True
			show = True
			if(len(bookings)==0):
				show1 = False
			if(len(ongoing)==0):
				show=False
			if(show==False and show1==False):
				messages.info(request,'No bokings done ')
				form = CheckRoom
				return HttpResponseRedirect('/' , {'form', form})
			return render(request , 'bookings.html' , {'bookings':bookings , 'delete':True , 'show':show ,'show':show , 'ongoing' : ongoing })
	else:
		messages.info(request,'Signin to delete bookings')
		return HttpResponseRedirect('/signinuser')

def bookings(request):
	global bookings
	if(auth and not m_auth):
		bookings = []
		ongoing = [] 
		al = Bookings.objects.all()
		for ty in al :
			if(ty.cid == auth_user.id):
				room = Rooms.objects.get(id=ty.rid)
				if(room.date<=datetime.date(datetime.now())):
					bookings.append((ty,room))
				else:
					ongoing.append((ty,room))
		show1 = True
		show = True
		if(len(bookings)==0):
			show1 = False
		if(len(ongoing)==0):
			show=False
		if(show==False and show1==False):
			messages.info(request,'No bokings done ')
			form = CheckRoom
			return HttpResponseRedirect('/' , {'form', form})
		return render(request , 'bookings.html' , {'bookings':bookings , 'delete':False , 'show':show ,'show':show , 'ongoing' : ongoing })
	else:
		messages.info(request,'Signin to delete bookings')
		return HttpResponseRedirect('/signinuser')

def bookroom1(request):
	form = CheckRoom
	if auth and not m_auth :
		if request.method=='POST':
			global st 
			global et
			d = datetime.strptime(request.POST['date'] , '%Y-%m-%d').date()
			st = int(request.POST['StartTime'])
			et = int(request.POST['EndTime'])
			if( d <  datetime.date(datetime.now()) ):
				messages.info(request,'Cannot book room in back date')
				return HttpResponseRedirect('/bookroom' , {'form':form })
			elif(st>=et):
				messages.info(request,'StartTime should be lesser than the EndTime')
				return HttpResponseRedirect('/bookroom' , {'form':form })			
			temp = Rooms.objects.all()
			for t in temp:
				if(t.status==False and t.date == d and t.addate<datetime.date(datetime.now())):
					print("here")
					if(t.startTime<=st and t.endTime>=et):
						print("here")
						rooms.append(t)
			if(len(rooms)==0):
				messages.info(request , "There are no rooms available with the given details")
				return HttpResponseRedirect('/bookroom' , {'form':form })
			return render(request,'bookroom.html' , {'form' : form,'rooms':rooms , 'rsize' : range(len(rooms)),'show':True})
	else:
		messages.info(request,'Login as user to book the room ')
		return HttpResponseRedirect('/signinuser')
	
def home(request):
	global rooms
	rooms=[]
	form = CheckRoom
	if request.method=='POST':
		d = datetime.strptime(request.POST['date'] , '%Y-%m-%d').date()
		global st 
		global et
		st = int(request.POST['StartTime'])
		et = int(request.POST['EndTime'])
		if( d <  datetime.date(datetime.now()) ):
			messages.info(request,'Cannot book room in back date')
			return HttpResponseRedirect('/' , {'form':form })
		elif(st>=et):
			messages.info(request,'StartTime should be lesser than the EndTime')
			return HttpResponseRedirect('/' , {'form':form })
		temp = Rooms.objects.all()
		for t in temp:
			if(t.status==False and t.date == d and t.addate<=datetime.date(datetime.now())):
				print("here")
				if(t.startTime<=st and t.endTime>=et):
					print("here")
					rooms.append(t)
		if(len(rooms)==0):
				messages.info(request , "There are no rooms available with the given details")
				return HttpResponseRedirect('/' , { 'form':form })
		return render(request,'home.html' , { 'table':True ,'form' : form ,'auth' : auth, 'user' : auth_user , 'manager':m_auth , 'rooms':rooms , 'rsize' : range(len(rooms))})
	else:
		return render(request,'home.html' , { 'table':False ,'form' : form , 'auth' : auth, 'user' : auth_user , 'manager':m_auth , 'rooms':rooms , 'rsize' : range(len(rooms))})

def signinmanager(request):
	form = CheckRoom
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
				return HttpResponseRedirect('/' , {'form', form})
		messages.info(request,'LoginIn Details are incorrect')
		return HttpResponseRedirect('/' , {'form', form})
	else:
		return render(request , 'signinmanager.html')

def signinuser(request):
	form = CheckRoom
	if request.method == 'POST':
		loginid = request.POST['loginid']
		password = request.POST['password']
		users = Customer.objects.all()
		for user in users:
			if(user.loginid==loginid and user.password == password):
				global auth 
				auth = True
				global m_auth 
				m_auth= False
				global auth_user
				auth_user = user
				print("verified")
				return HttpResponseRedirect('/' , {'form', form})
		messages.info(request,'LoginIn Details are incorrect')
		return HttpResponseRedirect('/' , {'form', form})
	else:
		return render(request , 'signinuser.html')

def signin(request):
	return render(request , 'signin.html')

def signup(request):
	return render(request , 'signup.html')

def signupuser(request):
	global regex
	form = Signup
	if request.method == 'POST':
		customers = Customer.objects.all()
		loginid = request.POST['loginid']
		if(len(loginid)<1):
			messages.info(request,'Loginid cant be empty')
			return HttpResponseRedirect('/signupuser')
		for customer in customers:
			if(customer.loginid == loginid):
				messages.info(request,'Loginid already taken')
				return HttpResponseRedirect('/signupuser' , {'form': form })

		password = request.POST['password']
		if(len(password)<8):
			messages.info(request,'Password too weak')
			return HttpResponseRedirect('/signupuser' ,{'form': form })

		name = request.POST['name']
		if(len(name)<1):
			messages.info(request,'Name cant be empty')
			return HttpResponseRedirect('/signupuser', {'form': form })
		email = request.POST['email']
		if(len(email)<1):
			messages.info(request,'Email cant be empty')
			return HttpResponseRedirect('/signupuser', {'form': form })
		elif(not re.search(regex,email)): 
			messages.info(request,'Email invalid')
			return HttpResponseRedirect('/signupuser' , {'form': form })
		customer = Customer(loginid = loginid , name = name , password = password , email = email)
		customer.save()
		print(customer.id)
		print("user created")
		return HttpResponseRedirect('/')
	else:
		return render(request , 'signupuser.html' , {'form': form })

def signupmanager(request):
	form = Signup
	if request.method == 'POST':
		customers = Customer.objects.all()
		loginid = request.POST['loginid']
		if(len(loginid)<1):
			messages.info(request,'Loginid cant be empty')
			return HttpResponseRedirect('/signupmanager')
		for customer in customers:
			if(customer.loginid == loginid):
				messages.info(request,'Loginid already taken')
				return HttpResponseRedirect('/signupmanager' , {'form': form })

		password = request.POST['password']
		if(len(password)<8):
			messages.info(request,'Password too weak')
			return HttpResponseRedirect('/signupmanager' ,{'form': form })

		name = request.POST['name']
		if(len(name)<1):
			messages.info(request,'Name cant be empty')
			return HttpResponseRedirect('/signupmanager', {'form': form })
		email = request.POST['email']
		if(len(email)<1):
			messages.info(request,'Email cant be empty')
			return HttpResponseRedirect('/signupmanager', {'form': form })
		elif(not re.search(regex,email)): 
			messages.info(request,'Email invalid')
			return HttpResponseRedirect('/signupmanager' , {'form': form })
		customer = Customer(loginid = loginid , name = name , password = password , email = email)
		customer.save()
		print(customer.id)
		print("user created")
		return HttpResponseRedirect('/')
	else:
		return render(request , 'signupmanager.html' , {'form': form })