import decimal

from django.contrib import admin
from .models import Topic, Course, Student, order, Review
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
 def reduce_price(modeladmin, request, queryset):
  for course in queryset:
   course.price = course.price * 90 / 100
   course.save()

 reduce_price.short_description = 'Apply 10%% discount'
 fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
 list_display = ('title', 'topic', 'price')
 actions = ['reduce_price']


 class Meta:
  model = Course

class OrderAdmin(admin.ModelAdmin):
 fields = [('courses'), ('student', 'order_status','order_date')]
 list_display = ('id', 'student', 'order_status', 'order_date','total_items')
 readonly_fields = ('order_date',)

class CourseInline(admin.TabularInline):
 model = Course

class TopicAdmin(admin.ModelAdmin):
 fields = [('name', 'length')]
 list_display = ('name','length')
 inlines = [ CourseInline]

class StudentAdmin(admin.ModelAdmin):
 fields = [('first_name', 'last_name', 'level','registered_courses')]
 list_display = ('first_name', 'last_name', 'level','get_courses')

 def get_courses(self, obj):
        return "\n".join([p.title for p in obj.registered_courses.all()])

# admin.site.register(Topic)
# admin.site.register(Course)
# admin.site.register(Student)
# admin.site.register(order)
admin.site.register(Review)
admin.site.register(Course, CourseAdmin)
admin.site.register(order, OrderAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Student, StudentAdmin)



