#!/usr/bin/env python3

import tweepy
import pandas as pd
import time
import math
import random
import copy
import configparser

config = configparser.ConfigParser()
config.read('config_twitter.ini')

CONSUMER_KEY = config['info']['CONSUMER_KEY']
CONSUMER_SECRET = config['info']['CONSUMER_SECRET']
ACCESS_TOKEN = config['info']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config['info']['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_list_members(list_idx):
	
    member_list = []

    delay_list = list(range(5, 9))

    for page in tweepy.Cursor(api.list_members, list_id = list_idx).pages():
        member_list.extend(page)
        time.sleep(random.choice(delay_list))

    print('No. of members in list ' + list_idx + ' is ' + str(len(member_list)))
    return member_list

    
def convert_df_save_csv(object_list, csv_name):
    all_users = [{'id': user.id,
                'Name': user.name,
                'Handle': user.screen_name,
                'Location': user.location,
                'Bio': user.description,
                'Account Protected':user.protected,
                'Followers Count': user.followers_count,
                'Following Count': user.friends_count,
                'Created on': user.created_at,
                'Lists present in': user.listed_count, 
                'Tweets Count': user.statuses_count}
                for user in object_list]

    converted_df = pd.DataFrame(all_users)

    converted_df.to_csv(csv_name, float_format='%f', index=False, encoding='utf-8')

    return converted_df


def add_members(list_to_add_to, list_of_ids_to_add):

    add_to_list_deepcopy = copy.deepcopy(list_of_ids_to_add)

    delay_list = list(range(31, 60))

    add_to_list_deepcopy_len = len(add_to_list_deepcopy)
    no_of_100s = math.ceil(add_to_list_deepcopy_len/100)

    for i in range(0, no_of_100s):
        print('doing ' + str(i) + ' * 100' )
        add_to_list_deepcopy_100 = add_to_list_deepcopy[:100]
        api.add_list_members(list_id=list_to_add_to, user_id=add_to_list_deepcopy_100)
        del add_to_list_deepcopy[:100]
        time.sleep(random.choice(delay_list))
    print('done and done')


def add_one_by_one(twitter_list_id, list_user_ids):

    delay_list = list(range(5, 9))
    for idx in list_user_ids:
        print(list_user_ids.index(idx))
        try:
            api.add_list_member(list_id = twitter_list_id, user_id=idx)
        except:
            print('issue with ' + str(idx))
        time.sleep(random.choice(delay_list))
    print('done and done')


def remove_members(list_to_remove_from, list_of_ids_to_remove):

    remove_from_list_deepcopy = copy.deepcopy(list_of_ids_to_remove)

    delay_list = list(range(31, 60))

    remove_from_list_deepcopy_len = len(remove_from_list_deepcopy)
    no_of_100s = math.ceil(remove_from_list_deepcopy_len/100)

    for i in range(0, no_of_100s):
        print('doing ' + str(i) + ' * 100' )
        remove_from_list_deepcopy_100 = remove_from_list_deepcopy[:100]
        api.remove_list_members(list_id=list_to_remove_from, user_id = remove_from_list_deepcopy_100)
        del remove_from_list_deepcopy[:100]
        time.sleep(random.choice(delay_list))
        
    print('done and done')


def remove_one_by_one(twitter_list_id, list_of_ids_4_removal):
    delay_list = list(range(5, 9))
            
    for idx in list_of_ids_4_removal:
        print(idx)
        try:
            api.remove_list_member(list_id = twitter_list_id, user_id = idx)
        except:
            print('issue with ' + str(idx))
        time.sleep(random.choice(delay_list))
    print('done and done')


def add_from_other_lists(list_to_add_to, other_lists):

    current_list_user_objects = get_list_members(list_to_add_to)
    current_list_user_ids = [user.id for user in current_list_user_objects]
    current_list_count = len(current_list_user_ids)
    print('At present, number of members in list is: ' + str(current_list_count))

    other_lists_user_objects = []

    for list_idx in other_lists:
        indiv_list_user_objects = get_list_members(list_idx)
        other_lists_user_objects.extend(indiv_list_user_objects)

    other_list_users_df = convert_df_save_csv(other_lists_user_objects, 'DELETE_ME.csv')

    
    other_list_users_df_no_dupli = other_list_users_df.drop_duplicates(subset=['id'])

    print('after removing duplicates, but before removing members already there, potentially members to be added: '\
            + str(len(other_list_users_df_no_dupli)))

    other_list_users_df_new = other_list_users_df_no_dupli[~other_list_users_df_no_dupli['id'].isin(current_list_user_ids)]

    print('After removing members already there, potentially ' + str(len(other_list_users_df_new)) + ' new members to be added')

    follower_limit = 5000

    users_with_huge_following = other_list_users_df_new[other_list_users_df_new['Followers Count'] >= follower_limit]

    users_with_less_following = other_list_users_df_new[other_list_users_df_new['Followers Count'] < follower_limit]

    print('Flagging ' + str(len(users_with_huge_following)) + ' users with huge following. Could be publications/organizations')

    print('Am saving to disk csv of users with huge following for checking')

    users_with_huge_following.to_csv('users_with_huge_following_for_manual_check.csv', float_format='%f', index=False, 
                                        encoding='utf-8')

    users_with_less_following_ids = users_with_less_following['id'].tolist()

    users_with_less_following_ids_count = len(users_with_less_following_ids)

    print('number of users to add to list is ' + str(users_with_less_following_ids_count))

    add_members(list_to_add_to, users_with_less_following_ids)

    new_member_list = get_list_members(list_to_add_to)
    new_member_list_count = len(new_member_list)

    discrepancy = new_member_list_count - (users_with_less_following_ids_count + current_list_count)

    print('After adding members, discrepancy is ' + str(discrepancy))
    
    print('done and done')