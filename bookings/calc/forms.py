from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class PasswordInput(forms.PasswordInput):
    input_type = 'password'

class CheckRoom(forms.Form):
    date = forms.DateField(widget=DateInput , label='Enter the Date   ')
    StartTime = forms.IntegerField(max_value=23 , min_value=0 , label='Start Time   ')
    EndTime = forms.IntegerField(max_value=24 , min_value=1 , label='End Time   ')


class AddRoomForm(forms.Form):
    number = forms.IntegerField(min_value=0)
    st = forms.IntegerField(max_value=23 , min_value=0)
    et = forms.IntegerField(max_value=24 , min_value=1)
    d = forms.DateField(widget=DateInput)
    upd = forms.DateField(widget=DateInput)
    ad = forms.IntegerField(min_value=0)

class Signup(forms.Form):
    loginid = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput())
    #password = forms.PasswordInput(widget=PasswordInput)
    name = forms.CharField(max_length=50)
    email = forms.EmailField()