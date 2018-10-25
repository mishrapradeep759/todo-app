# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import DomainGroup
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def get_user_email(user_id):
    user1 = get_object_or_404(User, pk=user_id)
    return user1.email

def create_user_domain(user_id):
    user_email = get_user_email(user_id)
    user_domain = user_email.split("@")[-1]
    return user_domain

def create_user_group():
    group = []
    users = User.objects.all()
    for user in users:
        group.append(create_user_domain(user.id))
    return group


