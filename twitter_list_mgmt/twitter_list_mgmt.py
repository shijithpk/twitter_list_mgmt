#!/usr/bin/env python3

# code from various stack overflow posts and github repos
    # took a lot of the authentication code from https://github.com/ravikiranj/twitter-challenge

# import tweepy
# import pandas as pd
# import time
# import math
# import random
# import copy
# import re
# import json

from .auth import getAPIHandle 
from .helpers import *

api = getAPIHandle().getAPI()


def add_to_list1_from_list2(list1, list2):
    """
    Adds members to twitter 'list1' from twitter 'list2'. You must own list1 to be able to add to it. 
    """
    # get user ids in list2 that arent there in list1
    difference = listA_minus_listB_difference(list2, list1)
    add_ids_to_list(difference, list1)


def add_to_list1_from_multiple_lists(list1, multiple_lists):
    """
    Adds users to twitter 'list1' from a list of twitter lists 'multiple_lists'. Note you cant have more than 5000 members in a list. 
    """
    union = union_of_lists(multiple_lists)
    add_to_list1_from_list2(list1, union)


def remove_from_list1_based_on_list2(list1, list2):
    """
    Removes users from 'list1' if they're also in 'list2'. Basically, this gets rid of the intersection from list1.
    """
    intersection = intersection_of_lists(list1,list2)
    remove_ids_from_list(intersection,list1)


def remove_from_list1_based_on_multiple_lists(list1,multiple_lists):
    """
    This removes users from 'list1' if they're also in any of the twitter lists in 'multiple_lists'.
    """
    union = union_of_lists(multiple_lists)
    intersection = intersection_of_lists(list1, union)
    remove_ids_from_list(intersection,list1)

def create_list_union(multiple_lists,list_name):
    """
    Creates a new list which has all the members from all the lists in 'multiple_lists'. Max of 5000 members for a list. 'list_name' is the name you're giving the new list.
    """
    union = union_of_lists(multiple_lists)
    response = api.create_list(name=list_name)
    response_dict = dictify_tweepy(response)
    new_list_id = response_dict['id_str']
    add_to_list1_from_list2(new_list_id, union)  

def create_list_intersection(multiple_lists,list_name):
    """
    Creates a new list which contains members common to all the lists in 'multiple_lists'. 'list_name' is the name you're giving the new list.
    """
    intersection = intersection_of_lists(multiple_lists)
    response = api.create_list(name=list_name)
    response_dict = dictify_tweepy(response)
    new_list_id = response_dict['id_str']
    add_to_list1_from_list2(new_list_id, intersection)

def create_list_difference(list1,multiple_lists,list_name):
    """
    Creates a new list which has all the members in list1 who arent in any of the lists in 'multiple_lists'. 'list_name' is the name you're giving the new list.
    """

    union = union_of_lists(multiple_lists)
    intersection = intersection_of_lists(list1, union)
    difference = listA_minus_listB_difference(list1,intersection)

    response = api.create_list(name=list_name)
    response_dict = dictify_tweepy(response)
    new_list_id = response_dict['id_str']
    add_to_list1_from_list2(new_list_id, difference)
