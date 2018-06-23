# these should be the only imports you need
import tweepy
import nltk
import json
import sys
import re


# write your code here
# usage should be python3 part1.py <username> <num_tweets>


# DEBUGGING FUNCTIONS

def retweets(timeline, originals):
	for tweet in timeline:
		print(tweet.full_text.encode("utf-8"))
		print("Favorites: " + str(tweet.favorite_count))
		print("Retweets: " + str(tweet.retweet_count))

	print("\nOriginal tweets")

	for tweet in originals:
		print(tweet.full_text.encode("utf-8"))
		print("Favorites: " + str(tweet.favorite_count))
		print("Retweets: " + str(tweet.retweet_count))


	print("\nNumber of tweets: " + str(len(timeline)))
	print("Number of original tweets: " + str(len(originals)))


# HELPER FUNCTIONS

def get_num_favorites(tweets):
	favorites = 0

	for tweet in tweets:
		favorites += tweet.favorite_count

	return favorites


def get_num_retweets(tweets):
	retweets = 0

	for tweet in tweets:
		retweets += tweet.retweet_count

	return retweets


def tag_freq_manager(tag, tag_dict):
	if tag not in tag_dict:
		tag_dict[tag] = 1
	else:
		tag_dict[tag] += 1


def top_tags(tag_dict, x_top):
	top_dict = {}
	output_str = ""
	iter_tracker = 0
	sorted_dict = sorted(tag_dict.items(), key=lambda x: (-x[1], x[0][0]))

	while iter_tracker < x_top and sorted_dict:
		top_tag = sorted_dict[0]

		if re.match(r'[a-zA-Z]+', top_tag[0]):
			top_dict[top_tag[0]] = top_tag[1]
			output_str += top_tag[0] + "(" + str(top_tag[1]) + ") " 
			iter_tracker += 1
			sorted_dict.remove(top_tag)
		else:
			sorted_dict.remove(top_tag)

	return (top_dict, output_str)


# MAIN PROGRAM

# Authentication information
consumer_key = "PBIlrjlF0XLwekPRSERDvik9z"
consumer_secret = "e0S6EuSckXiuscQ85PMtvmYGhqp2u79yMilJw0Zgw7KpeHpYQ2"
access_token = "1271117575-FyoJHLw1v44NW0jOZ4LscksZdDafg7fdxNmOu8r"
access_token_secret = "jtAgCimjBekEdtYXnGY5i7qLuOVqbJ0tb8B4g9T0Sk9Di"


# Authenticate tweepy and grab the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Get the command-line arguments
user = sys.argv[1]
num_tweets = sys.argv[2]


# Grab the given number of tweets
timeline = api.user_timeline(screen_name=user, count=num_tweets, tweet_mode='extended')


# Grab the original tweets from the timeline
originals = []
all_text = []

for tweet in timeline:
	text = tweet.full_text

	if text[:7].find("RT @"):
		originals.append(tweet)

	all_text.append(text.split())

# retweets(timeline, originals) # Double-check results


# Get the total favorites and retweets
num_favorites = get_num_favorites(originals)
num_retweets = get_num_retweets(originals)


# Analyze text of tweets. Start by removing stopwords and then tagging
stopwords = set(nltk.corpus.stopwords.words("english"))
extra_stopwords = ['RT']
bad_strings = ['@', '#', 'http', 'https']

for word in extra_stopwords:
	stopwords.add(word)

all_words = ""
append_flag = True

for line in all_text:
	for word in line:

		append_flag = True

		if not re.search(r'[a-zA-Z]+', word):
			append_flag = False

		if word in stopwords:
			append_flag = False

		for bad_string in bad_strings:
			if not word.find(bad_string):
				append_flag = False

		if append_flag:
			all_words += word + " "

tagset = nltk.pos_tag(nltk.tokenize.word_tokenize(all_words))

vb_dict = {} # Verb dict
nn_dict = {} # Noun dict
jj_dict = {} # Adjective dict

top_verb = "" # Most common verb
top_noun = "" # Most common noun
top_adj = "" # Most common adjective

for tag in tagset:

	if tag[1][:2] == 'VB':
		tag_freq_manager(tag[0], vb_dict)
	elif tag[1][:2] == 'NN':
		tag_freq_manager(tag[0], nn_dict)
	elif tag[1][:2] == 'JJ':
		tag_freq_manager(tag[0], jj_dict)


vb_output = ""
nn_output = ""
jj_output = ""

top_vb_dict, vb_output = top_tags(vb_dict, 5)
top_nn_dict, nn_output = top_tags(nn_dict, 5)
top_adj_dict, jj_output = top_tags(jj_dict, 5)


# Create and write a CSV file of the most common nouns

with open('noun_data.csv', 'w', newline='') as file:

	file.write("Noun,Number\n")

	for noun in top_nn_dict:
		file.write(noun + "," + str(top_nn_dict[noun]) + "\n")


# Print output

print("USER: " + user)
print("TWEETS ANALYZED: " + str(num_tweets))
print("VERBS: " + vb_output)
print("NOUNS: " + nn_output)
print("ADJECTIVES: " + jj_output)
print("ORIGINAL TWEETS: " + str(len(originals)))
print("TIMES FAVORITED (ORIGINAL TWEETS ONLY): " + str(num_favorites))
print("TIMES RETWEETED (ORIGINAL TWEETS ONLY): " + str(num_retweets))