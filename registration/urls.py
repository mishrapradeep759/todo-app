from django.conf.urls import url
from django.shortcuts import redirect, render, reverse
from . import views as user_view

app_name="registration"

urlpatterns = [

    url(r'^$', user_view.registration_page, name="registration"),
]