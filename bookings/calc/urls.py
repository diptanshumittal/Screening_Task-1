from django.urls import path, include
from . import views

urlpatterns = {
	path('',views.home , name = 'home'),
	path('add',  views.add , name='add'),
	path('accounts/login',  views.login , name='accounts/login'),
	path('accounts/register',  views.register , name='accounts/register'),
}