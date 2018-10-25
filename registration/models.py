# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group

#
# class DomainGroup(Group):
#     title = models.CharField(max_length=200)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username

class NavigationPannel(models.Model):
    assign_task = models.CharField(max_length=200)
    view_task = models.CharField(max_length=200)


    # @property
    # def username(self):
    #     return self.user.username
