# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.models import User, Group
from .models import Profile
from .models import TaskManager

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from registration.forms import TaskForm, LoginForm, RegistrationForm



def send_request_to_admin(request):
    return get_pending_request(request)


def get_pending_request(request):
    pending_requests = Profile.objects.filter(is_active=False)
    return render(request, "registration/pending_requests.html", {"pending_requests": pending_requests})

def user_login(request):
    if request.method=="POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            email = data["email"]
            password = data["password"]
            username = data["username"]
            user = authenticate(request, username=username, password=password)
            print user.profile
            if user is not None:
                print "user is admin %s" % user.profile.is_admin
                if user.profile.is_active==True:

                    login(request, user)

                    return redirect(reverse("registration:profile", args=(user.profile.id,)))

                else:
                    return HttpResponse("Request is pending")

    else:
        login_form = LoginForm()

    return render(request, "registration/login.html", {"form": login_form})


def user_profile(request, user_id):

    users = Profile.objects.filter(is_active=False)
    admin_user = Profile.objects.filter(is_admin=True, is_active=True)

    return render(request, "registration/user.html", {"users": users, "admin_user": admin_user})


def registration_page(request):
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
            print "created %s" % created

            if created:
                profile.is_admin = True
                profile.is_active = True
                profile.save()

            return redirect(reverse("registration:registration_completed"))

    else:
        registration_form = RegistrationForm()
    return render(request, "registration/registration.html", {"registration_form": registration_form})


def home_view(request):
    return render(request, "registration/home.html")


def reistration_completed(request):
    return render(request, "registration/registration_completed.html")


def approve_user(request, user_id):

    user_profile = Profile.objects.get(user__id=user_id)
    user_profile.is_active=True
    user_profile.save()
    return redirect(reverse('registration:pending_requests'))


def home(request):
    return redirect(reverse("registration:logout"))

@login_required
def add_task(request):
    if request.method=="POST":
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            _form = form.save(commit=False)
            _form.assignor=request.user
            _form.save()
            return redirect(reverse("registration:taskboard"))
    else:
        form=TaskForm(request.user)
    return render(request, "registration/task.html", {"form": form})

@login_required
def taskboard(request):
    if request.user.profile.is_admin:
        tasks = TaskManager.objects.filter(assignee__profile__group=request.user.profile.group)
    else:
        tasks = TaskManager.objects.filter(assignee=request.user)
    context = {'tasks': tasks, 'user': request.user}
    return render(request, "registration/taskboard.html", context)


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

