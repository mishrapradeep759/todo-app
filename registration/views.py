# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, redirect, get_object_or_404
from user_registration_form import UserCreationForm


def registration_page(request):

    registration_form = UserCreationForm(   )
    return render(request, "registration/registration.html")