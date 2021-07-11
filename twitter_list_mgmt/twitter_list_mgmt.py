#!/usr/bin/env python3

# code from various stack overflow posts and github repos
    # took a lot of the authentication code from https://github.com/ravikiranj/twitter-challenge

from .auth import getAPIHandle 
from .helpers import *

api = getAPIHandle().getAPI()

def add_to_list1_from_list2(list1, list2):
    """
    Adds to twitter 'list1' all members of twitter 'list2'. 
    
    Here 'list1' and 'list2' are the twitter list ids. \n
    You must own list1 to be able to add to it. 
    """
    list2_ids = get_okay_list_members_ids(list2)
    add_ids_to_list(list2_ids, list1)


def add_to_list1_from_multiple_lists(list1, multiple_lists):
    """
    Adds to twitter 'list1' members from all lists in 'multiple_lists'. 
    
    Here, 'multiple_lists' is a python list of twitter list ids. \n
    'list1' is a twitter list id. \n
    Note you cant have more than 5000 members in a list. 
    """
    union = union_of_lists(multiple_lists)
    add_ids_to_list(union, list1)


def remove_from_list1_based_on_list2(list1, list2):
    """
    Removes users from 'list1' if they're also in 'list2'. 
    
    Here 'list1' and 'list2' are twitter list ids. \n
    """
    list2_ids = get_okay_list_members_ids(list2)
    remove_ids_from_list(list2_ids,list1)


def remove_from_list1_based_on_multiple_lists(list1,multiple_lists):
    """
    This removes users from twitter 'list1' if they're in any of the lists in 'multiple_lists'.

    Here, 'list1' is a twitter list id.\n
    'multiple_lists' is a python list of twitter list ids.
    """
    union = union_of_lists(multiple_lists)
    remove_ids_from_list(union,list1)


def create_list_union(multiple_lists,list_name):
    """
    Creates a new list that has the members of all the lists in 'multiple_lists'. 
    
    Here, 'multiple_lists' is a python list of twitter list ids.\n
    'list_name' is the name you're giving the new list.\n
    A list can have a maximum of 5000 members. 
    """
    union = union_of_lists(multiple_lists)
    response = api.create_list(name=list_name, mode='private')
    response_dict = dictify_tweepy(response)
    new_list_id = response_dict['id_str']
    add_ids_to_list(union, new_list_id)
    print('New list created at https://twitter.com/i/lists/' + new_list_id)


def create_list_intersection(multiple_lists,list_name):
    """
    Creates a new list of members common to all the lists in 'multiple_lists'. 
    
    Here, 'multiple_lists' is a python list of twitter list ids.\n
    'list_name' is the name you're giving the new list.
    """
    intersection = intersection_of_lists(multiple_lists)

    response = api.create_list(name=list_name, mode='private')
    response_dict = dictify_tweepy(response)
    new_list_id = response_dict['id_str']
    add_ids_to_list(intersection, new_list_id)
    
    print('New list created at https://twitter.com/i/lists/' + new_list_id)


def create_list_difference(list1,multiple_lists,list_name):
    """
    Creates a new list of members from 'list1' who aren't in any list in 'multiple_lists'.
     
    Here, 'list1' is a twitter list id.\n
    'multiple_lists' is a python list of twitter list ids.\n
    'list_name' is the name you're giving the new list.
    """
    union = union_of_lists(multiple_lists)

    list1_ids = get_okay_list_members_ids(list1)

    difference_as_set = set(list1_ids).difference(set(union))
    difference = list(difference_as_set)

    response = api.create_list(name=list_name, mode='private')
    response_dict = dictify_tweepy(response)
    new_list_id = response_dict['id_str']
    add_ids_to_list(difference, new_list_id)
    print('New list created at https://twitter.com/i/lists/' + new_list_id)
