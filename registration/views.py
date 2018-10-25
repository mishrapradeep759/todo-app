# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, redirect, get_object_or_404
from registration_form import RegistrationForm
from .models import Profile
from django.contrib.auth.models import User,Group
from django.http import HttpResponse




def send_request_to_admin(request):
    return get_pending_request(request)

def get_pending_request(request):
    pending_requests = Profile.objects.filter(user__is_active="False")
    return render(request, "registration/pending_requests.html", {"pending_requests": pending_requests})

def show_request_message(request):
    return HttpResponse("<h1>Your request has been pending by admin</h1>")

    # return acess_to_user(request,user_id)


def registration_page(request):
    print request.method

    if request.method=="POST":
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            data = registration_form.cleaned_data
            email = data["email"]
            domain = email.split("@")[-1]
            group, created = Group.objects.get_or_create(name=domain)
            user = registration_form.save(commit=False)
            registration_form.save()
            profile = Profile.objects.create(user=user, group=group)

            if created:
                profile.is_admin = True
                profile.is_active = True
                profile.save()
            else:
                profile.save()
                return send_request_to_admin(request)

            return redirect(reverse("registration:login"))

    else:
        registration_form = RegistrationForm()
    return render(request, "registration/registration.html", {"registration_form": registration_form})


'''once the user is register, request should go to admin, once he aproves this function get called'''
def acess_to_user(request, user_id):

    user_profile = Profile.objects.get(user__id=user_id)
    user_profile.is_active=True


def home(request):
    return redirect(reverse("registration:logout"))


def user_login(request):
    return render(request, "registration/home.html")


def get_user_email(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return user.email


def create_user_domain(request, user_id):
    user_email = get_user_email(request, user_id)
    user_domain = user_email.split("@")[-1]
    return user_domain


def create_user_group(request):
    group = []
    users = User.objects.all()
    for user in users:
        group.append(create_user_domain(request, user.id))
    return render(request, "registration/group.html", {'group': group})

# def check_domain(request):
#     logged_in_user = request.user
#     domain1 = get_object_or_404(DomainGroup, pk=1)
#
#     return HttpResponse(domain1.users.all())