from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import order, Review, Student, Course


class SearchForm(forms.Form):
 LENGTH_CHOICES = [
 (8, '8 Weeks'),
 (10, '10 Weeks'),
 (12, '12 Weeks'),
 (14, '14 Weeks'),
 ]
 name = forms.CharField(max_length=100, required=False, label = 'Student Name')
 length = forms.TypedChoiceField(widget=forms.RadioSelect, choices = LENGTH_CHOICES, coerce=int, required= False, label='Preferred course duration:')
 max_price = forms.IntegerField(label='Maximum Price', min_value=0 )


class OrderForm(forms.ModelForm):
 class Meta:
  model = order
  fields = ['courses', 'student', 'order_status']
  widgets = {'courses': forms.CheckboxSelectMultiple(),'order_type':forms.RadioSelect}
  labels = {'student': u'Student Name', }


class ReviewForm(forms.ModelForm):
 class Meta:
  model = Review
  fields = ['reviewer', 'course', 'rating', 'comments']
  widgets = {'course': forms.RadioSelect, 'comments': forms.Textarea}
  labels = {'reviewer': u'Please enter a valid email', 'rating':'Rating: An integer between 1 (worst) and 5 (best)' }


class RegisterForm(UserCreationForm):
 def __init__(self, *args, **kwargs):
  super(RegisterForm, self).__init__(*args, **kwargs)
  # do not require password confirmation
  del self.fields['password2']

 class Meta:
  model = Student
  fields = ['username', 'first_name', 'last_name', 'province', 'interested_in']

  widgets = {
   'interested_in': forms.CheckboxSelectMultiple,
  }

  labels = {
   'first_name': 'First Name',
   'last_name': 'Last Name',
   'interested_in': 'Interested In'
  }


class LoginForm(forms.Form):
 username = forms.CharField(max_length=100)
 password = forms.CharField(widget=forms.PasswordInput())