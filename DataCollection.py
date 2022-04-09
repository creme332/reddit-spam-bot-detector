# -*- coding: utf-8 -*-
import praw

reddit = praw.Reddit(
)

# Code written to collect Reddit usernames of bots and real people

def check_if_user_exists(name):
    try:
        reddit.redditor(name).created
        return True
    except :
        return False
    return False
    
def ExtractNames():
    BotUsernames = set()
    with open("RedditBotNames.txt") as file: #contained a list of bots from https://www.reddit.com/r/botwatch/comments/1wg6f6/bot_list_i_built_a_bot_to_find_other_bots_so_far/cf1nu8p/ 
        for line in file:
            name = line.split()[0][3:]
            if check_if_user_exists(name):
                BotUsernames.add(name)
    file.close()
    
    f = open("CleanRedditBot.txt", "a")
    for name in BotUsernames :
        f.write(name+'\n')
    f.close()
    print(len(BotUsernames))

def FindRealRedditors():
    PersonUsername = set()
    for subreddit in reddit.subreddits.default(limit=20):
        if(len(PersonUsername)>300) :
            break
        if(subreddit.subscribers>500000): 
            for post in subreddit.top(limit=20):
                if(check_if_user_exists(post.author)):    
                    PersonUsername.add(post.author)
                    
    f = open("CleanRedditor.txt", "a")
    for name in PersonUsername :
        f.write(str(name) +'\n')
    f.close()
    print(len(PersonUsername))
ExtractNames()
FindRealRedditors()
