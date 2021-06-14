from django.urls import path
from django.views.generic import detail
from myfileF20 import settings
from django.conf.urls.static import static

from myapp.views import index, detail
from myapp import views

app_name = 'myapp'

urlpatterns = [
 path(r'login/', views.user_login, name='login'),
 path(r'logout/', views.user_logout, name='logout'),
 path(r'myaccount/', views.myaccount, name='myaccount'),
 path(r'register/', views.register, name='register'),
 path(r'', index.as_view(), name='index'),
 path(r'about/', views.about, name='about'),
 path(r'<int:topic_id>/', detail.as_view(), name='detail'),
 path(r'findcourses/', views.findcourses, name='findcourses'),
 path(r'place_order/', views.place_order, name='place_order'),
 path(r'order_response/', views.place_order, name='place_order'),
 path(r'review/', views.review, name='review'),
 path(r'myorder/', views.myOrder, name='myOrder'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)