from urllib.parse import urlencode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
# Import necessary classes
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View

from .models import Topic, Course, Student, order, Review, User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm, OrderForm, ReviewForm, LoginForm, RegisterForm


# Create your views here.
# def index(request):
#  top_list = Topic.objects.all().order_by('id')[:10]
#  return render(request, 'Lab3App/index.html', {'top_list': top_list})

class index(View):
    def get(self, request):
        last_login = 'You are logged out'
        if request.session.get('last_login', False):
            last_login = datetime.strptime(request.session.get('last_login'), '%Y-%m-%d %H:%M:%S')
            time_elasped = datetime.now() - last_login
            if time_elasped.seconds > 3600:
                # its been more than hour
                logout(request)
                last_login = 'Your last login was more than one hour ago'
            else:
                pass
        else:  # you are not logged in
            pass
        top_list = Topic.objects.all().order_by('id')[:10]
        return render(request, 'myapp/index.html', {
            'top_list': top_list,
            'last_login': last_login,
        })


def about(request):
    if 'about_visits' in request.COOKIES.keys():
        about_visits = request.COOKIES['about_visits']
    else:
        about_visits = 1
    if about_visits:
        about_visits = int(about_visits) + 1
    else:
        about_visits = 1
    response = render(request, 'myapp/about.html', {'about_visits': about_visits})
    response.set_cookie('about_visits', value=about_visits, max_age=300)
    return response


class detail(View):
    def get(self, request, topic_id):
        top_list = Topic.objects.get(id=topic_id)
        course_list = Course.objects.filter(topic_id=top_list.id)
        return render(request, 'myapp/detail.html', {'top_list': top_list, 'course_list': course_list})


# Lab8
def findcourses(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            price = form.cleaned_data['max_price']
            if length:
                topics = Course.objects.filter(price__lt=price, topic__length=length)
            else:
                topics = Course.objects.filter(price__lt=price)

            courselist = list(topics.all())
            return render(request, 'myapp/results.html', {'courselist': courselist, 'name': name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
    return render(request, 'myapp/findcourses.html', {'form': form})


# Lab9
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save()
            student = order.student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)

            return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
        else:
            return render(request, 'myapp/place_order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})


@login_required
def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if request.user.is_authenticated:
            try:
                student = Student.objects.get(id=request.user.id)
                if student.LVL_CHOICES == 1 or student.LVL_CHOICES == 2:
                    if form.is_valid():
                        course = form.cleaned_data['course']
                        rating = form.cleaned_data['rating']
                        reviewer = form.cleaned_data['reviewer']
                        comments = form.cleaned_data['comments']
                        review = Review(course=course, reviewer=reviewer, rating=rating, comments=comments)
                        if rating >= 1 and rating <= 5:
                            course.num_reviews = course.num_reviews + 1
                            course.save()
                            review.save()
                            return HttpResponseRedirect('/Lab3App')
                        else:
                            form.add_error('rating', "You must enter a rating between 1 and 5")
                            return render(request, 'myapp/review.html', {'form': form})
                    else:
                        return render(request, 'myapp/review.html', {'form': form})
            except:
                form.add_error('reviewer', 'You must be registered in Undergraduate or Post graduate to submit review')
                return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


# Lab10
def user_login(request):
    context = {}
    context['form'] = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session['last_login'] = last_login
                request.session.set_expiry(3600)
                if 'next' in request.POST:
                    return redirect('myapp:' + request.POST.get('next'))
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required(login_url="myapp:login")
def myaccount(request):
    user = request.user

    student = Student.objects.filter(pk=user.pk)
    if student.count() == 0:
        return render(request, 'myapp/myaccount.html', {'message': "You're not a registered student."})
    else:
        return render(request, 'myapp/myaccount.html',
                      {'first_name': student.get().first_name, 'last_name': student.get().last_name,
                       'topics': student.get().interested_in.all(), 'courses': student.get().registered_courses.all()})



@login_required
def myOrder(request):
    user = request.user
    student = Student.objects.filter(pk=user.pk)
    if student.count() == 0:
        return render(request, 'myapp/myorder.html', {'message': "You're not a registered student."})
    else:
        return render(request, 'myapp/myorder.html', {'orders': student.get().students.all()})


# if request.user.is_authenticated:
#   student = Student.objects.get(id=request.user.id)
#  if student:
#     user = get_object_or_404(Student, pk=request.user.id)
#    order_list =order.objects.filter(student__user=user)
#   print(order_list)
#  if order_list.exists():
#     return render(request, 'myapp/myorder.html', {'user': user,'order_list': order_list})
# else:
#   return HttpResponse("you have not ordered anything yet")
# else:
#   return HttpResponse("User not found")
# except:
#   return HttpResponse("you are not registered as a student")


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')

    form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
