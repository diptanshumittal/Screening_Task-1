from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class HomeForm(forms.Form):
    date = forms.DateField(widget=DateInput , label='Enter the Date   ')
    StartTime = forms.IntegerField(max_value=23 , min_value=0 , label='Start Time   ')
    EndTime = forms.IntegerField(max_value=24 , min_value=1 , label='End Time   ')


