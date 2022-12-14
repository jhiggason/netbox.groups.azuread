# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Jeff Higgason <jeff.higgason@erickson.is>
# All rights reserved
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#
# Author: Jeff Higgason <jeff.higgason@erickson.is>

"""Additional social.auth pipeline to process an AzureAD user."""
import logging
from django.contrib.auth.models import Group

logger = logging.getLogger("netbox.auth.Azure") #Log to /var/log/netbox/netbox.log under the tag "netbox.auth.Azure"
ROLES_GROUP_NAME = "roles" #Name of the dictionary key(group) we are looking for in the AzureAD "response"
SUPERUSER_GROUPS = ["admins"] #Name of the AzureAD "App Role" that we will use to assign SuperUsers to Django and Netbox *Note Django Admins need both superuser flag and staff flag set to get access to the Django admin console
STAFF_GROUPS = ["staff"] #name of the AzureAD "App Role" that we will use to assign users to the "staff" group in Netbox


def group_sync(uid, user=None, response=None, *args, **kwargs):  # Define a function called group_sync for assigning AzureAD users to Netbox and Django groups
    """Sync the App Roles and groups from AzureAD and Django and set staff/superuser as appropriate."""
    if user and response and response.get(ROLES_GROUP_NAME, False):
        group_memberships = response.get(ROLES_GROUP_NAME)
        is_staff = False
        is_superuser = False
        logger.info(f"User {uid} is a member of {', '.join(group_memberships)}, Logging in from IP: {response.get('ipaddr')}") #Log who is trying to log in- what app roles are assigned- and what IP Address they are signing in from.
        # Make sure all groups exist in Netbox
        group_ids = []  #Create a blank list
        for group in group_memberships:
            if group in SUPERUSER_GROUPS: #If a user is added to the AzureAD app role "admins"- set the Superusers and Staff flag in Django giving them access to the Django admin console 
                is_superuser = True #Set user to have all write/change permissions available
                is_staff = True #Allow user access to the Django Admin Console
            group_ids.append(Group.objects.get_or_create(name=group)[0].id) #Ensure that both the "admins" and "staff" groups exsist in netbox
        user.groups.set(group_ids) #Set the user's group in netbox to either "staff" or both "staff" and "admins" - depending on app role membership (App Role = staff will assign only the staff group in netbox-- App Role = admins will set both admins and staff group in netbox)
        user.is_superuser = is_superuser #Set admins as superusers in Django
        user.is_staff = is_staff #Set admins as staff in Django- this allows acess to the Django admin console 
        user.save() #Save it
    else:
        logger.info(f"Did not receive roles from Azure, response: {response}")

"""This is used in 2 locations
- /netbox/netbox/netbox/settings.py around line 295 
- /netbox/netbox/netbox/configuration.py around line 223
"""
