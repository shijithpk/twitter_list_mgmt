### About the repo 

This is a python package for adding and removing members from a twitter list using *other* twitter lists.

Say you've created a covid twitter list to keep track of news around the pandemic. You've just found a curated list on covid by an epidemiologist in London, and you want to add members from that list to your own Covid list. This is the package you use for that.

This package will help heavy twitter and tweetdeck users, especially those those who use lists to manage the firehose of information that is social media.

Have also written a [blog post](http://shijith.com/blog/twitter-list-management/) about why I coded this, but this README covers pretty much everything you need to know.


### How to install the package and set things up

You can install it by going to the terminal and typing  
```
pip install twitter_list_mgmt
```

Versions of Tweepy >= 4.0.0a0 are required for this package to work. At the time of writing, 4.0 is in alpha, so it might not be available from [pypi](https://pypi.org/project/tweepy/#history). Install it in the terminal by doing
```
pip install git+https://github.com/tweepy/tweepy.git
```

In terms of setting up, you'll have to [create](https://developer.twitter.com/) authentication credentials for yourself. (This [article](https://realpython.com/twitter-bot-python-tweepy/) from Realpython has a how-to on it.) Four text strings will be generated -- Consumer Key, Consumer Secret, Access Token and Access Token Secret. Create a file named 'config_twitter.ini', use the format below and paste in the credentials (You can also download a sample file [here](twitter_list_mgmt/config_twitter.ini))

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

There are 7 main methods in the package:  

1. This method allows you to add members to one of your lists from another list. Here list1 and list2 are twitter list ids, with list1 being the one you own. (You can get the ids from the url for a list page. For example, in the url https://twitter.com/i/lists/15299140, the list id is '15299140'.)
```
tlm.add_to_list1_from_list2(list1, list2)
```

2. This is the same as the previous method, just that it adds to your list from several lists. 'multiple_lists' is a python list of twitter list ids.
```
tlm.add_to_list1_from_multiple_lists(list1, multiple_lists)
```

3. Remove members from your list who are in another list with this method, 'list1' being your list. Let's say you have a twitter list that's a mix of designers and developers, and you want it to have designers only. You can remove many of the developers from it by getting a curated list of developers. Using this function, if any developer's in that list, they'll be removed from your list.
```
tlm.remove_from_list1_based_on_list2(list1, list2)
```

4. This removes members from your list using several other twitter lists.
```
tlm.remove_from_list1_based_on_multiple_lists(list1,multiple_lists)
```

5. This creates a new list that consolidates members from several lists. 'multiple_lists' is the python list containing the twitter list ids and 'list_name' is the name for the new list.
```
tlm.create_list_union(multiple_lists,list_name)
```

6. This creates a new list that has members common to several lists. 'multiple_lists' is the python list containing the twitter list ids and 'list_name' is the name for the new list.
```
tlm.create_list_intersection(multiple_lists,list_name)
```

7. This creates a new list which has all the members from 'list1' who aren't in any of the lists in 'multiple_lists'. 'list1' can be your own list or someone else's, 'multiple_lists' is a python list of twitter list ids and 'list_name' is the name for the new list.
```
tlm.create_list_difference(list1,multiple_lists,list_name)
```

### Other things you can do

The methods that have been listed are the main ones. There are other methods too, but most people won't have a need for them. Will go through some of them for coders who want to create their own functions based on them. (Have a look at [helpers.py](twitter_list_mgmt/helpers.py) to see how they've been defined.)

These are some of the other methods:  
  
* This one helps automate the fetching of list ids from list urls. Returns the list_id as a string.
```
tlm.get_list_id_from_url(url)
```

* Get all the members of a twitter list. The function returns a python list of their user ids.
```
tlm.get_list_members_ids(list_idx)
```

* Add user ids to a list you own. 'ids' here is a python list of user ids and 'list1' is the id for your twitter list.
```
tlm.add_ids_to_list(ids,list1)
```

* Remove user ids from a list you own. 'ids' here is a python list of user ids and 'list1' is the id for your twitter list.
```
tlm.remove_ids_from_list(ids,list1)
```

* Create a pandas dataframe from a list, with each row a different member and each column an attribute like number of followers, number of tweets posted etc. This is for anyone who wants to analyze the membership of a list.
```
tlm.get_df_from_list(list_idx)
```

### Suggestions, criticism etc.
I'm not a professional coder/developer/programmer, so am sure there are things here I should be doing differently. If you have any suggestions, please contact me on mail@shijith.com or at my twitter handle [@shijith](https://twitter.com/shijith).

For example, I would be especially interested in hearing about my python application layout, whether it could be simplified further, if I could be doing imports better etc.
