# -*- coding: utf-8 -*-
import praw
from datetime import datetime
from datetime import date


reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
    username = "",
    password = "",
)

#user = reddit.redditor('snoocockbot') #an actual bot
user = reddit.redditor('Most-Boring-Bot') # an actual bot

#user = reddit.redditor('carbonatedcoochie2') #a  real person

def AccountAge() :
    birthday = datetime.utcfromtimestamp(user.created_utc)
    today = date.today()
    #print(today.year, today.month, today.day)
    #print(date.year, date.month, date.day)

    years = today.year - birthday.year
    months =  today.month - birthday.month
    
    if(months<0):
        years-=1
        months+=12
        
    days = today.day -  birthday.day
    
    if(days<0):
        days+=31
        months-=1

    if(months<0):
        years-=1
        months+=12
    result = "Account's age : " + str(years) + " years " + str(months) + " months " + str(days) + " days"
    return result # uncertainty : +- 1 day

def HasVerifiedEmail():
     if(user.has_verified_email):
         return 50
     return -10
 
def AnalysePostsSimilarity(PostLimit):
    UniquePosts = set() 
    UniqueTitle =  set()
    postsAnalysed_count=0 # count number of posts when user has posted < PostLimit

    for post in user.submissions.new(limit=PostLimit):
        UniquePosts.add(post.selftext)
        postsAnalysed_count+=1
        UniqueTitle.add(post.title)
        print(post.title)
    return 100*(postsAnalysed_count- len(UniquePosts))/postsAnalysed_count + 100*(postsAnalysed_count- len(UniqueTitle))/postsAnalysed_count

def TimeDifference(t1, t2):
    #t1 and #t2 are in utc format
    d1 = datetime.utcfromtimestamp(t1)
    d2 = datetime.utcfromtimestamp(t2)
    
    date1 = datetime(d1.year, d1.month, d1.day,d1.hour,d1.minute,d1.second)
    date2 = datetime(d2.year, d2.month, d2.day,d2.hour,d2.minute,d2.second)
    return (abs(date2 - date1).days)

def PostingInterval(NumberOfPostsAnalysed):
    IsFirstComment=1
    PreviousTime = 0 # previous post's date
    days_interval= []
    time_interval=[]
    sum_of_intervals= 0
    for post in user.submissions.new(limit=NumberOfPostsAnalysed):
        if IsFirstComment :
            IsFirstComment=0
            PreviousTime = post.created_utc
        else :
            current_interval = TimeDifference(PreviousTime, post.created_utc)
            sum_of_intervals += current_interval
            days_interval.append(current_interval)
            PreviousTime = post.created_utc
    mean_interval = sum_of_intervals / len(days_interval)
    print(days_interval)
    print(mean_interval)
    variance = 0
    for i in range(0, len(days_interval)):
        variance += (days_interval[i]-mean_interval)**2
    variance /= (len(days_interval)-1)
    print (variance)
def CommentInterval():
    return 0
def FinalReport():
    PostLimit=5
    totalscore = HasVerifiedEmail() + AccountAge() +AnalysePostsSimilarity(PostLimit)
    return totalscore

PostingInterval(5)
#print(AnalysePostsSimilarity(100))
