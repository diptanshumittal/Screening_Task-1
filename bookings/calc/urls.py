from django.urls import path, include
from . import views

urlpatterns = {
	path('',views.home , name = 'home'),
	path('add',  views.add , name='add'),
	path('logout',  views.logout , name='logout'),
	path('signin',  views.signin , name='signin'),
	path('signinuser',  views.signinuser , name='signinuser'),
	path('signinmanager',  views.signinmanager , name='signinmanager'),
	path('signup',  views.signup , name='signup'),
	path('signupuser',  views.signupuser , name='signupuser'),
	path('signupmanager',  views.signupmanager , name='signupmanager'),
	path('addroom',  views.addroom , name='addroom'),
}