from django.contrib import admin
from django.urls import path
from fullsite.views import home,login,sendMessage,admin_chat
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login,name='login'),
    path('home/',home,name='home'),
    path('message/',sendMessage,name='message'),
    path('adminchat/',admin_chat,name='admin_chat')
]

