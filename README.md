### About the repo 

`twitter_list_mgmt` is a python package that makes it easier to add users to your twitter list from other lists.

Say you've created a covid twitter list to keep track of news around the pandemic. You've just found another list on covid curated by an epidemiologist in London, and you want to add members from that to your own Covid list. This is the package you use for it.

Now for most basic operations like retrieving the current membership of a Twitter list, adding users to it, removing them etc. the [Tweepy](https://github.com/tweepy/tweepy) library is good enough. `twitter_list_mgmt` just adds extra functionality on top of Tweepy to make working with lists easier.

This package will help heavy twitter and tweetdeck users, especially those who use lists to manage the firehose of information from social media.

### List of functions 

Here's what you can do with the `twitter_list_mgmt` package:
* Main functions
    * [Add members to your list from another list](#1)
    * [Add members to your list from multiple lists](#2)
    * [Remove members from your list who are in another list](#3)
    * [Remove members from your list who are in any of multiple other lists](#4)
    * [Create a new list that combines members from multiple lists](#5)
    * [Create a new list that has members common to multiple lists](#6)
    * [Create a new list with members from a list, who aren't in any of multiple other lists](#7)
* Other functions
    * [Get the list id from a list url](#8)
    * [Get all the user ids of list members](#9)
    * [Add user ids to a list](#10)
    * [Remove user ids from a list](#11)
    * [Create a pandas dataframe from a list](#12)


### How to install the package and set things up

Versions of Tweepy >= 4.0.0a0 are required for this package to work. At the time of writing, 4.0.0 isn't available in [pypi](https://pypi.org/project/tweepy/#history). Install it from the terminal by doing
```
pip install git+https://github.com/tweepy/tweepy.git
```

Then install the main package by going to the terminal and typing  
```
pip install twitter_list_mgmt
```

In terms of setting up, you'll have to [create](https://developer.twitter.com/) authentication credentials for yourself. (This [article](https://realpython.com/twitter-bot-python-tweepy/) from Realpython has a how-to on it.) Four text strings will be generated -- Consumer Key, Consumer Secret, Access Token and Access Token Secret. Create a file named 'config_twitter.ini', use the format below and paste in the credentials without apostrophes. You can also download a sample file [here](twitter_list_mgmt/config_twitter.ini). Place the config in the same directory and on the same level as your script.

```
[info]
CONSUMER_KEY = XXXXXX
CONSUMER_SECRET = XXXXXX
ACCESS_TOKEN = XXXXXX
ACCESS_TOKEN_SECRET = XXXXXX
```

### How to use the package  
  
Import the package into your code with
```
import twitter_list_mgmt as tlm
```

The package has **7** main functions:  

**1.** <a name="1"></a>**Add members to your list from another list** — Here 'list1' and 'list2' are twitter list ids, with list1 being the one you own. (You can get the ids from the url for a list page. For example, in the url https://twitter.com/i/lists/15299140, the list id is '15299140'.)
```
tlm.add_to_list1_from_list2(list1, list2)
```

**2.** <a name="2"></a>**Add members to your list from several other lists** — 'multiple_lists' is a python list of twitter list ids. (To comply with Twitter's rate limits, only upto 1000 members can be added in a day.)
```
tlm.add_to_list1_from_multiple_lists(list1, multiple_lists)
```

**3.** <a name="3"></a>**Remove members from your list who are in another list** — Let's say you have a twitter list on covid that's a mix of experts and journalists, and you want it to have experts only. Now you can remove many of the journalists from it manually, but you can also do it in an automated fashion by getting a list of science/health journalists. Using this function, if any of your list members are on that journalist list, they'll be removed. 'list1' here is your list id.
```
tlm.remove_from_list1_based_on_list2(list1, list2)
```

**4.** <a name="4"></a>**Remove members from your list who are in any of the other lists specified** — 'list1' here is your list id and 'multiple_lists' is a python list of twitter list ids.
```
tlm.remove_from_list1_based_on_multiple_lists(list1,multiple_lists)
```

**5.** <a name="5"></a>**Create a new list that combines members from several lists** — 'multiple_lists' is the python list containing the twitter list ids and 'list_name' is the name for the new list. (The Twitter list created is set as 'private' but can be made 'public' later.)
```
tlm.create_list_union(multiple_lists,list_name)
```

**6.** <a name="6"></a>**Create a new list that has members common to several lists** — 'multiple_lists' is the python list containing the twitter list ids and 'list_name' is the name for the new list.
```
tlm.create_list_intersection(multiple_lists,list_name)
```

**7.** <a name="7"></a>**Create a new list with all the members from a list, who aren't in any of the other lists specified** — 'list1' can be your own list or someone else's, 'multiple_lists' is a python list of twitter list ids and 'list_name' is the name for the new list.
```
tlm.create_list_difference(list1,multiple_lists,list_name)
```

### Other things you can do

The functions that have been listed are the main ones. There are others too, but most people won't need them. Will go through some of those functions for coders who want to build something on top of them. (Go through [helpers.py](twitter_list_mgmt/helpers.py) to see how they've been defined.)

These are some of the other functions:  
  
* **Get the list id from a list url**<a name="8"></a>  — Extracts the list_id and returns it as a string.
```
tlm.get_list_id_from_url(url)
```

* **Get all the members of a list**<a name="9"></a>  — The function returns a python list of their user ids. Tweepy has a similar function [`get_list_members`](https://docs.tweepy.org/en/latest/api.html#tweepy.API.get_list_members) but that retrieves user objects. This function goes a step further by extracting the user ids within those objects.
```
tlm.get_list_members_ids(list_idx)
```

* **Add user ids to a list**<a name="10"></a>  — 'ids' here is a python list of user ids and 'list1' is a twitter list id.
```
tlm.add_ids_to_list(ids,list1)
```

* **Remove user ids from a list**<a name="11"></a>  — 'ids' here is a python list of user ids and 'list1' is a twitter list id.
```
tlm.remove_ids_from_list(ids,list1)
```

* **Create a pandas dataframe from a list**<a name="12"></a>  — Here, each row is for a different member and each column an attribute like number of followers, number of tweets posted etc. This is for anyone who wants to analyze the membership of a list.
```
tlm.create_df_from_list(list_idx)
```

### Suggestions, criticism etc.
I'm not a professional developer/programmer/coder, so am sure there are things here I should be doing differently. If you have any suggestions, please contact me on mail@shijith.com or at my twitter handle [@shijith](https://twitter.com/shijith).

For example, I would be interested in hearing about my python application layout. Whether it could be simplified further, if I could be doing imports better etc.
