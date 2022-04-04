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
    check_for_async=False
)

#user = reddit.redditor('snoocockbot')
#user = reddit.redditor('snoocockbot')
user = reddit.redditor('carbonatedcoochie2')

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
         return "Account has no verified email"
     return "Account has a verified email"
 
def CommentSimilarity(NumberOfPostsAnalysed):
    count = {} # map declaration
    uniquecomments=0

    for comment in user.submissions.new(limit=NumberOfPostsAnalysed):
        print(comment.created_utc)
        if comment in count.keys(): #if element is present in map
            count[comment]+=1
        else : # element not present in map
            count[comment] = 1 # add a new element to a map 
            
    for c in count:
        uniquecomments+=1
    percentage =  100*(NumberOfPostsAnalysed - uniquecomments)/NumberOfPostsAnalysed
    return str(percentage)+ "% of its " + str(NumberOfPostsAnalysed)+ " latest posts were identical"

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
    interval= []
    for post in user.submissions.new(limit=NumberOfPostsAnalysed):
        if IsFirstComment :
            IsFirstComment=0
            PreviousTime = post.created_utc
        else :
            interval.append(TimeDifference(PreviousTime, post.created_utc))
            PreviousTime = post.created_utc
    
    print(interval)
def CommentInterval():
    return 0
def FinalReport():
    NumberOfPostsAnalysed=5
    print(AccountAge())  
    print(CommentSimilarity(NumberOfPostsAnalysed))
    print(HasVerifiedEmail())
    print(user.icon_img)


PostingInterval(5)
