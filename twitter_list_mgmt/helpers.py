#!/usr/bin/env python3

import tweepy
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
    Takes the tweepy user object and converts it into a dictionary, makes it easier to extract values from.
    """
    json_str = json.dumps(tweepy_object._json)
    return json.loads(json_str)


def get_list_members_ids(list_idx):
    """
    Given a twitter 'list_idx', this gets all the members of that list. It returns a python list of twitter user ids, the twitter user ids being strings here and not integers.
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
    Given a twitter list id, gets all the members of that twitter list. It returns a python list of twitter user ids, the twitter user ids being strings here and not integers. Users that have protected profiles and whom you don't follow already, won't be included
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
    Finds all the users in lists in 'multiple_lists'. It returns a list of ids for all those users. If a user's profile is protected, they're only added if the authenticated user, ie. you, are following them now.
    """

    member_dict_lists_merged = []

    for listx in multiple_lists:
        member_object_list = api.get_list_members(list_id=listx, count=5000)
        member_dict_list = [dictify_tweepy(member_object) for member_object in member_object_list]
        member_dict_lists_merged.extend(member_dict_list)
        time.sleep(5)

    member_id_list = []

    for member_dict in member_dict_lists_merged:
        member_protected = member_dict['protected']
        current_user_follows_member = member_dict['following']
        if member_protected:
            if not current_user_follows_member:
                continue
        member_id = member_dict['id_str']
        member_id_list.append(member_id)

    union = list(set(member_id_list))

    return union


def intersection_of_lists(multiple_lists):
    """
    Finds the users common to all lists in 'multiple_lists'. It returns a list of ids for those common users. If a user's profile is protected, they're only added if the authenticated user, ie. you, are following them now.
    """

    member_id_lists_collection = []

    for listx in multiple_lists:
        member_object_list = api.get_list_members(list_id=listx, count=5000)
        time.sleep(5)
        member_dict_list = [dictify_tweepy(member_object) for member_object in member_object_list]
        member_id_list = []
        for member_dict in member_dict_list:
            member_protected = member_dict['protected']
            current_user_follows_member = member_dict['following']
            if member_protected:
                if not current_user_follows_member:
                    continue
            member_id = member_dict['id_str']
            member_id_list.append(member_id)
        member_id_lists_collection.append(member_id_list)
    
    intersection_set = set(member_id_lists_collection[0]).intersection(*member_id_lists_collection[1:])

    intersection = list(intersection_set)

    return intersection


def listA_minus_listB_difference(listA,listB):
    """
    Returns a list of ids from 'listA' which are not in 'listB'
    """

    listA_ids = get_okay_list_members_ids(listA)
    time.sleep(5)
    listB_ids = get_okay_list_members_ids(listB)

    difference_as_set = set(listA_ids).difference(set(listB_ids))
    difference = list(difference_as_set)

    return difference


def add_ids_to_list(ids,list1):
    """
    Adds 'ids' -- a list of twitter user ids -- to a twitter 'list1'. Note that lists have a limit of 5,000 members. Also, because of twitter's rate limits, you can only add around 1,000-1,400 users to a list in a day. Think the precise limit is 1,440 (from 24*60, 1 user a minute over 24 hours), the limit might be different for different people. FIND OUT WHAT THE LIMIT IS FOR YOU
    """

    no_of_users_to_add = len(ids)
    limit_for_users_added_in_a_day = 1000

    if no_of_users_to_add < limit_for_users_added_in_a_day:
        add_to_list_deepcopy = copy.deepcopy(ids)
        delay_list = list(range(31, 60))
        add_to_list_deepcopy_len = len(add_to_list_deepcopy)
        no_of_100s = math.ceil(add_to_list_deepcopy_len/100)

        for i in range(0, no_of_100s):
            add_to_list_deepcopy_100 = add_to_list_deepcopy[:100]
            api.add_list_members(list_id=list1, user_id=add_to_list_deepcopy_100)
            del add_to_list_deepcopy[:100]
            time.sleep(random.choice(delay_list))
    else:
        time_min = (5 * len(ids))/60
        time_max = (9 * len(ids))/60
        print('This will take {} - {} minutes'.format(time_min, time_max))
        #CHECK IF 5-9 SECONDS IS ENOUGH OF A DELAY TO HAVE PROCESS COMPLETE FOR ALL IDS
        delay_list = list(range(5, 9))
        for idx in ids:
            try:
                api.add_list_member(list_id =list1, user_id=idx)
            except:
                print('issue with twitter id ' + str(idx))
            time.sleep(random.choice(delay_list))

def remove_ids_from_list(ids,list1):
    """
    Removes 'ids' -- a list of twitter user ids -- from a twitter 'list1'. THINK THERE MIGHT BE A LIMIT FOR NUMBER OF MEMBERS THAT CAN BE REMOVED IN A DAY. FIND OUT WHAT THE LIMIT IS FOR YOU
    """

    no_of_users_to_remove = len(ids)
    limit_for_users_removed_in_a_day = 1000

    if no_of_users_to_remove < limit_for_users_removed_in_a_day:
        remove_from_list_deepcopy = copy.deepcopy(ids)
        remove_from_list_deepcopy_len = len(remove_from_list_deepcopy)
        no_of_100s = math.ceil(remove_from_list_deepcopy_len/100)

        delay_list = list(range(31, 60))
        
        for i in range(0, no_of_100s):
            remove_from_list_deepcopy_100 = remove_from_list_deepcopy[:100]
            api.remove_list_members(list_id=list1, user_id = remove_from_list_deepcopy_100)
            del remove_from_list_deepcopy[:100]
            time.sleep(random.choice(delay_list))

    else:
        delay_list = list(range(5, 9))
        #CHECK IF 5-9 SECONDS IS ENOUGH OF A DELAY TO HAVE PROCESS COMPLETE FOR ALL IDS
        for idx in ids:
            try:
                api.remove_list_member(list_id = list1, user_id = idx)
            except:
                print('issue with ' + str(idx))
            time.sleep(random.choice(delay_list))


# convenience method. Dont really use it anywhere, but might be helpful for end-user
def get_list_id_from_url(url):
    """
    Given a twitter list url, extracts the list id from it through regex, and returns the list id as a string.
    So given the url 'https://twitter.com/i/lists/1295996537449771008' , you get back '1295996537449771008'
    """
    regex_pattern = r'https:\/\/twitter\.com\/i\/lists\/([0-9]+)$'
    list_id = re.match(regex_pattern, url).group(1)
    return list_id


def create_df_from_list(list_idx):
    """
    This takes a twitter_list 'list_idx' and converts it into a pandas dataframe for analysis. 
    """
    member_object_list = api.get_list_members(list_id=list_idx, count=5000)
    
    all_members = []

    for member in member_object_list:
        member_dict = dictify_tweepy(member)
        all_members.append(member_dict)

    converted_df = pd.DataFrame(all_members)

    return converted_df