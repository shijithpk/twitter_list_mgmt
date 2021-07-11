#!/usr/bin/env python3

import pandas as pd
import time
import math
import random
import copy
import re
import json
import random
from .auth import getAPIHandle 

api = getAPIHandle().getAPI()

# function to convert _json to JSON
def dictify_tweepy(tweepy_object):
    """
    Takes a tweepy user object and converts it into a dictionary.
    
    A dictionary makes it easier to extract values from.
    """
    json_str = json.dumps(tweepy_object._json)
    return json.loads(json_str)


def get_list_members_ids(list_idx):
    """
    Given a twitter list id, returns a python list of user ids for all the list members.
    
    Note that the user ids in the returned python list will be strings and not integers.
    """
    member_object_list = api.get_list_members(list_id=list_idx, count=5000)

    member_id_list = []

    for member in member_object_list:
        member_dict = dictify_tweepy(member)
        member_id = member_dict['id_str']
        member_id_list.append(member_id)

    return member_id_list

def get_okay_list_members_ids(list_idx):
    """
    Given a twitter list id, returns a python list of user ids for all the list members.
    
    Users that have protected profiles and whom you don't follow won't be included.
    """
    member_object_list = api.get_list_members(list_id=list_idx, count=5000)

    member_id_list = []

    for member in member_object_list:
        member_dict = dictify_tweepy(member)
        member_protected = member_dict['protected']
        current_user_follows_member = member_dict['following']
        if member_protected:
            if not current_user_follows_member:
                continue
        member_id = member_dict['id_str']
        member_id_list.append(member_id)

    return member_id_list


def union_of_lists(multiple_lists):
    """
    Returns a python list of user ids for members of all lists in 'multiple_lists'. 
    
    Here, 'multiple_lists' is a python list of twitter list ids.\n
    Users that have protected profiles and whom you don't follow won't be included.
    """
    member_id_list = []

    for listx in multiple_lists:
        listx_ids = get_okay_list_members_ids(listx)
        member_id_list.extend(listx_ids)

    union = list(set(member_id_list))

    return union



def intersection_of_lists(multiple_lists):
    """
    Returns a python list of user ids for members common to all lists in 'multiple_lists'. 
    
    Here, 'multiple_lists' is a python list of twitter list ids.\n
    Users that have protected profiles and whom you don't follow won't be included.
    """
    member_id_lists_collection = []

    for listx in multiple_lists:
        listx_ids = get_okay_list_members_ids(listx)
        member_id_lists_collection.append(listx_ids)
    
    intersection_set = set(member_id_lists_collection[0]).intersection(*member_id_lists_collection[1:])
    intersection = list(intersection_set)

    return intersection



def listA_minus_listB_difference(listA,listB):
    """
    Returns a python list of user ids for members of 'listA' who are not in 'listB'

    Here, 'listA' and 'listB' are twitter list ids.
    """

    listA_ids = get_okay_list_members_ids(listA)
    time.sleep(5)
    listB_ids = get_okay_list_members_ids(listB)

    difference_as_set = set(listA_ids).difference(set(listB_ids))
    difference = list(difference_as_set)

    return difference



def add_ids_to_list(ids,list1):
    """
    Adds 'ids'-- a python list of twitter user ids-- to a twitter 'list1'.

    Here, 'list1' is a twitter list id.\n
    Note that lists have a limit of 5,000 members. \n
    Also, because of twitter's rate limits, you can only add around 900-1500 users to a list in a day. \n
    Crossing this limit will get you blocked from adding members to this and other lists. \n
    An internal limit of 1,000 is used to ensure that doesn't happen.
    """
    list1_ids = get_okay_list_members_ids(list1)
    ids_to_add_set = set(ids).difference(set(list1_ids))
    ids_to_add = list(ids_to_add_set)

    no_of_users_to_add = len(ids_to_add)
    limit_for_users_added_in_a_day = 1000

    if no_of_users_to_add > limit_for_users_added_in_a_day:
        print("There are {} users to add. To comply with Twitter's rate limits, 1000 users--or even less--will be added today. Add the rest after 24 hours.".format(no_of_users_to_add))
        ids_to_add = ids_to_add[0:1000]

    add_to_list_deepcopy = copy.deepcopy(ids_to_add)
    add_to_list_deepcopy_len = len(add_to_list_deepcopy)
    no_of_100s = math.ceil(add_to_list_deepcopy_len/100)

    for i in range(0, no_of_100s):
        add_to_list_deepcopy_100 = add_to_list_deepcopy[:100]
        api.add_list_members(list_id=list1, user_id=add_to_list_deepcopy_100)
        del add_to_list_deepcopy[:100]
        time.sleep(3)


def remove_ids_from_list(ids,list1):
    """
    Removes members from a twitter list 'list1' if their user id is in 'ids', a python list of user ids.
    
    Here, 'list1' is a twitter list id.
    """

    list1_ids = get_okay_list_members_ids(list1)

    intersection_set = set(list1_ids).intersection(ids)
    ids_to_remove = list(intersection_set)

    remove_from_list_deepcopy = copy.deepcopy(ids_to_remove)
    remove_from_list_deepcopy_len = len(remove_from_list_deepcopy)
    no_of_100s = math.ceil(remove_from_list_deepcopy_len/100)
    
    for i in range(0, no_of_100s):
        remove_from_list_deepcopy_100 = remove_from_list_deepcopy[:100]
        api.remove_list_members(list_id=list1, user_id = remove_from_list_deepcopy_100)
        del remove_from_list_deepcopy[:100]


# convenience method. Dont really use it anywhere, but might be helpful for end-user
def get_list_id_from_url(url):
    """
    Given a twitter list url, extracts the list id from it and returns it as a string.

    So given the url 'https://twitter.com/i/lists/1295996537449771008', you get back '1295996537449771008'
    """
    regex_pattern = r'https:\/\/twitter\.com\/i\/lists\/([0-9]+)$'
    list_id = re.match(regex_pattern, url).group(1)
    return list_id


def create_df_from_list(list_idx):
    """
    This takes a twitter list id 'list_idx' and converts it into a pandas dataframe for analysis. 

    The function returns the pandas dataframe.
    """
    member_object_list = api.get_list_members(list_id=list_idx, count=5000)
    
    all_members = []

    for member in member_object_list:
        member_dict = dictify_tweepy(member)
        all_members.append(member_dict)

    converted_df = pd.DataFrame(all_members)

    return converted_df