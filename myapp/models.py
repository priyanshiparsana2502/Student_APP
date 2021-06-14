from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "%i/" % self.id


def validate_price(value):
    if value < 50 or value > 500:
        raise ValidationError(
            ('%(value)s should be between $50 and $500'), params={'value': value},
        )


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(validators=[MaxValueValidator(500),MinValueValidator(50)], max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]
    is_staff = True
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True)
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    profile_pic = models.ImageField(upload_to='media/', default='media/noimage.png')


    def __str__(self):
        return self.first_name


class order(models.Model):
    ORDER_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Confirmed'),
        (2, 'On Hold')
    ]
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    courses = models.ManyToManyField(Course, blank=True)
    student = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE)
    order_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '{} by {} '.format(self.student, self.courses.all())

    def total_items(self):
        count = 0
        for order in self.courses.all():
            count = count + 1
        return count

    def total_cost(self):
        cost = 0
        for course in self.courses.all():
            cost = cost + course.price
        return cost


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.reviewer
