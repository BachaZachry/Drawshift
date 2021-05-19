"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from page.views import home_view
from page.views import contact_view
from tasks.views import task_detail_view,task_create_view,dynamic_lookup_view,dynamic_delete_view,task_list_view
urlpatterns = [
    path('tasks/',include('tasks.urls')),
    path('admin/', admin.site.urls),
      path('task/',task_list_view,name='task'),
    path('task/<int:id>/deletee',dynamic_delete_view,name='task-delete'),
        path('task/<int:id>/',dynamic_lookup_view,name='task-detail'),

    path('create/',task_create_view),
    path('',home_view,name='home'),
     path('contact/',contact_view,name='contact'),
        path('api/', include('rest_framework.urls'))
]
