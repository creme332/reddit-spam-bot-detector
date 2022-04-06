# -*- coding: utf-8 -*-
import praw
from datetime import datetime
from datetime import date

import math

reddit = praw.Reddit(
)

#user = reddit.redditor('snoocockbot') #an actual bot
user = reddit.redditor('Most-Boring-Bot') # an actual bot

#user = reddit.redditor('carbonatedcoochie2') #a real person

def AnalyseAccountAge() :
    # analyse account age, in days
    # age inversely proportional to likelihood of being a bot
    d1 = datetime.utcfromtimestamp(user.created_utc)
    d2 = date.today()
    totaldays = abs(d1.year*365 + 31* d1.month + d1.day - (d2.year*365 + 31* d2.month + d2.day))
    print(totaldays)
    if totaldays==0:
        return 20
    if(totaldays<31) : # an account less than 1 month old is sus
        return totaldays
    return 0
def HasVerifiedEmail():
     if(user.has_verified_email):
         return 50
     return -10
 
def AnalysePostsSimilarity(PostLimit):
    #analyse post title and post content for similarity
    UniquePosts = set() 
    UniqueTitle =  set()
    postsAnalysed_count=0 # count number of posts when user has posted < PostLimit

    for post in user.submissions.new(limit=PostLimit):
        UniquePosts.add(post.selftext)
        postsAnalysed_count+=1
        UniqueTitle.add(post.title)
    return 100*(postsAnalysed_count- len(UniquePosts))/postsAnalysed_count + 100*(postsAnalysed_count- len(UniqueTitle))/postsAnalysed_count

def TimeDifference(t1, t2, ReturnDays):
    #t1 and #t2 are in utc format
    d1 = datetime.utcfromtimestamp(t1)
    d2 = datetime.utcfromtimestamp(t2)
    
    date1 = datetime(d1.year, d1.month, d1.day,d1.hour,d1.minute,d1.second)
    date2 = datetime(d2.year, d2.month, d2.day,d2.hour,d2.minute,d2.second)
    if(ReturnDays): #return difference in days
        return (abs(date2 - date1).days)
    
    #return difference in time in seconds
    return abs((3600*date1.hour + 60*date1.minute + date1.second) - (3600*date2.hour + 60*date2.minute + date2.second))

def PostingInterval(NumberOfPostsAnalysed):
    # analyse time interval between each post
    IsFirstComment=1
    previous_date = 0 # previous post's date
    days_interval= [] # difference in time between consecutive posts, measured in days
    time_interval=[] # difference in time between consecutive post time, measured in seconds
    
    for post in user.submissions.new(limit=NumberOfPostsAnalysed):
        if IsFirstComment :
            IsFirstComment=0
            previous_date = post.created_utc
        else :
            current_interval = TimeDifference(previous_date, post.created_utc,1)
            days_interval.append(current_interval)
            time_interval.append(TimeDifference(previous_date, post.created_utc,0))
            previous_date = post.created_utc
    
    #calculate variance for days_interval
    mean_days_interval = sum(days_interval)/ len(days_interval)
    days_variance = 0
    for i in range(0, len(days_interval)):
        days_variance += (days_interval[i]-mean_days_interval)**2
    days_variance /= (len(days_interval)-1)
    
    #calculate variance for time_interval
    mean_time_interval = sum(time_interval)/ len(time_interval)
    time_variance=0;
    for i in range(0,len(time_interval)):
        time_variance += (time_interval[i]-mean_time_interval)**2
    
    weight = 0 
    if(math.sqrt(time_variance)< 100) : #posts around the same time 
        weight+=math.sqrt(time_variance)*3
    if(math.sqrt(days_variance)<3): #posts at most every 3 days
        weight+= math.sqrt(days_variance)*2
    return weight #if weight=0, program cannot identify redditor's posting pattern

def CommentInterval():
    #analyse time interval between comments
    return 0
def AnalyseComments(NumberOfPostsAnalysed):
    #check comments' content for similarity
    UniqueComments =  set() #stores comments' content
    postsAnalysed_count = 0
    for comment in user.comments.new(limit=NumberOfPostsAnalysed):
        UniqueComments.add(comment.body)
        postsAnalysed_count+=1
    return 100*(postsAnalysed_count- len(UniqueComments))/postsAnalysed_count 
 
def FinalReport():
    PostLimit=5
    totalscore = HasVerifiedEmail() + AnalyseAccountAge() + AnalysePostsSimilarity(PostLimit)
    totalscore += PostingInterval(PostLimit)
    return totalscore

#print(PostingInterval(5))
#print(AnalysePostsSimilarity(100))
#print(user.created_utc)

print(AnalyseAccountAge())
#print(AnalyseComments(10))
