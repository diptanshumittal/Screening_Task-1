from django.urls import path, include
from . import views

urlpatterns = {
	path('',views.home , name = 'home'),
	path('logout',  views.logout , name='logout'),
	path('signin',  views.signin , name='signin'),
	path('signinuser',  views.signinuser , name='signinuser'),
	path('signinmanager',  views.signinmanager , name='signinmanager'),
	path('signup',  views.signup , name='signup'),
	path('signupuser',  views.signupuser , name='signupuser'),
	path('signupmanager',  views.signupmanager , name='signupmanager'),
	path('addroom',  views.addroom , name='addroom'),
	path('bookroom',  views.bookroom , name='bookroom'),
	path('bookroom1',  views.bookroom1 , name='bookroom1'),
	path('bookings',  views.bookings , name='bookings'),
	path('deletebookings',  views.deletebookings , name='deletebookings'),
	path('changeslots',  views.changeslots , name='changeslots'),
	path('viewbookings',  views.viewbookings , name='viewbookings'),
}