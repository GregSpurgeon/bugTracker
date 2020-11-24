"""tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from bugs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ticketform/', views.create_ticket_view, name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail_view, name='ticket_page'),
    path('status_done/<int:ticket_id>/', views.ticket_done_view),
    path('status_new/<int:ticket_id>/', views.ticket_new_view),
    path('assignticket/<int:ticket_id>/', views.assign_ticket_view),
    path('status_invalid/<int:ticket_id>/', views.ticket_invalid_view),
    path("myuser/<int:myuser_id>/", views.myuser_detail_view, name='myuser_detail'),
    path('edit/<int:pk>/', views.edit_ticket_view)
]
