# -*- coding: utf-8 -*-
import praw
from datetime import datetime
from datetime import date

import math

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
    username = "",
    password = ""
)

def AnalyseAccount(user) :
    # analyse account age, in days and the karma count
    # age inversely proportional to likelihood of being a bot
    # 
    d1 = datetime.utcfromtimestamp(user.created_utc)
    d2 = date.today()
    totaldays = abs(d1.year*365 + 31* d1.month + d1.day - (d2.year*365 + 31* d2.month + d2.day))
    weight = 0
    if totaldays==0:
        return 20
    if(totaldays<31) : # an account less than 1 month old is sus
        weight += totaldays
    else:
        if(user.comment_karma + user.link_karma < 100): 
            weight += 10
    
    if(user.has_verified_email):
         weight -= 10
    else:
         weight += 50 #bots are less likely to have verified emails
         
    return weight 
def AnalysePosts(user, PostLimit):
    #analyse post title and post content for similarity
    UniquePosts = set() 
    UniqueTitle =  set()
    postsAnalysed_count=0 # count number of posts when user has posted < PostLimit

    for post in user.submissions.new(limit=PostLimit):
        UniquePosts.add(post.selftext)
        postsAnalysed_count+=1
        UniqueTitle.add(post.title)
        
    if(postsAnalysed_count>0):
        return 100*(postsAnalysed_count- len(UniquePosts))/postsAnalysed_count + 100*(postsAnalysed_count- len(UniqueTitle))/postsAnalysed_count
    return 0
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

def PostingInterval(user, NumberOfPostsAnalysed):
    # analyse time interval between each post
    IsFirstComment=1
    previous_date = 0 # previous post's date
    days_interval= [] # difference in time between consecutive posts, measured in days
    time_interval=[] # difference in time between consecutive post time, measured in seconds
    postsAnalysed_count=0 # count number of posts when user has posted < PostLimit

    for post in user.submissions.new(limit=NumberOfPostsAnalysed):
        postsAnalysed_count+=1
        if IsFirstComment :
            IsFirstComment=0
            previous_date = post.created_utc
        else :
            current_interval = TimeDifference(previous_date, post.created_utc,1)
            days_interval.append(current_interval)
            time_interval.append(TimeDifference(previous_date, post.created_utc,0))
            previous_date = post.created_utc
            
    weight = 0
    if postsAnalysed_count>0 :
        if len(days_interval)>1:
            #calculate variance for days_interval
            mean_days_interval = sum(days_interval)/ len(days_interval)
            days_variance = 0
            for i in range(0, len(days_interval)):
                days_variance += (days_interval[i]-mean_days_interval)**2
            days_variance /= (len(days_interval)-1)
            #print(days_interval)
            #print(days_variance)
            if(math.sqrt(days_variance)<3): 
                weight+= 20
        
        if len(time_interval)>1:
            #calculate variance for time_interval
            mean_time_interval = sum(time_interval)/ len(time_interval)
            time_variance=0;
            for i in range(0,len(time_interval)):
                time_variance += (time_interval[i]-mean_time_interval)**2
            time_variance /= (len(time_interval)-1)
            #print(time_interval)
            #print(time_variance)
        
            if(math.sqrt(time_variance)>0) :  
                weight+= 400/math.sqrt(time_variance)

    return weight

def CommentInterval(user, NumberOfPostsAnalysed):
    # analyse time interval between each comment
    IsFirstComment=1
    previous_date = 0 # previous comment's date
    days_interval= [] # difference in time between consecutive comments, measured in days
    time_interval=[] # difference in time between consecutive comments, measured in seconds
    
    for comment in user.comments.new(limit=NumberOfPostsAnalysed):
        if IsFirstComment :
            IsFirstComment=0
            previous_date = comment.created_utc
        else :
            days_interval.append(TimeDifference(previous_date, comment.created_utc,1))
            time_interval.append(TimeDifference(previous_date, comment.created_utc,0))
            previous_date = comment.created_utc
    
    weight = 0 
    #calculate variance for days_interval
    if len(days_interval) > 1 :
        mean_days_interval = sum(days_interval)/ len(days_interval)
        days_variance = 0
        for i in range(0, len(days_interval)):
            days_variance += (days_interval[i]-mean_days_interval)**2
        days_variance /= (len(days_interval)-1)
        if(math.sqrt(days_variance)<3):
            weight+= 20
            
    #calculate variance for time_interval
    if len(time_interval) > 1 :
        mean_time_interval = sum(time_interval)/ len(time_interval)
        time_variance=0;
        for i in range(0,len(time_interval)):
            time_variance += (time_interval[i]-mean_time_interval)**2
        time_variance /= (len(time_interval)-1)
        #print(time_interval)
        #print(time_variance)
        if(math.sqrt(time_variance)>0) : 
            weight+=400/math.sqrt(time_variance)
    
    return weight #if weight=0, program cannot identify redditor's posting pattern

def AnalyseComments(user, NumberOfPostsAnalysed):
    #check comments' content for similarity
    UniqueComments =  set() #stores comments' content
    CommentsAnalysed_count = 0
    for comment in user.comments.new(limit=NumberOfPostsAnalysed):
        UniqueComments.add(comment.body)
        CommentsAnalysed_count+=1
    if(CommentsAnalysed_count>0):
        return 100*(CommentsAnalysed_count- len(UniqueComments))/CommentsAnalysed_count 
    return 0
def BotScore(username, PostLimit):
    user= reddit.redditor(username)
    totalscore = 0
    totalscore += AnalyseAccount(user) 
    totalscore += AnalysePosts(user,PostLimit)
    totalscore += PostingInterval(user, PostLimit)
    totalscore += AnalyseComments(user, PostLimit)
    totalscore += CommentInterval(user, PostLimit)
    #return totalscore
    print(totalscore)
    if(totalscore<85):
        return False # not a bot
    return True

def FindThresholdOfBotScore():
    
    PostLimit = 5 # upperbound for number of posts to be analysed for each account
    AccountLimit = 10 # upperbound for number of accounts to be analysed
    
    AllBotScores = []
    i=0
    with open("CleanRedditBot.txt") as file:
        for user in file:
            if(i>=AccountLimit):
                break
            currentScore = BotScore(reddit.redditor(user),PostLimit)
            AllBotScores.append((currentScore))
            i+=1
    file.close()
    AllBotScores.sort()
    #print minimum median, mean, max
    print(AllBotScores[0],AllBotScores[int(len(AllBotScores)/2)], sum(AllBotScores)/len(AllBotScores),AllBotScores[len(AllBotScores)-1] )

    AllHumanScores=[]
    i=0
    with open("CleanRedditor.txt") as file:
        for user in file:
            if(i>=AccountLimit):
                break
            currentScore = BotScore(reddit.redditor(user),PostLimit)
            AllHumanScores.append((currentScore))
            i+=1
    file.close()
    
    AllHumanScores.sort()
    print(AllHumanScores[0],AllHumanScores[int(len(AllHumanScores)/2)], sum(AllHumanScores)/len(AllHumanScores), AllHumanScores[len(AllHumanScores)-1])


def EvaluateAlgorithm():
    PostLimit = 60 # upperbound for number of posts to be analysed for each account
    AccountLimit = 900# upperbound for number of accounts to be analysed
    
    i=0
    correct=0
    with open("CleanRedditBot.txt") as file:
        for user in file:
            if(i>=AccountLimit):
                break
            if BotScore(reddit.redditor(user),PostLimit):
                correct+=1
            i+=1
    file.close()
    print(100*correct/i)
    
    j=0
    with open("CleanRedditor.txt") as file:
        for user in file:
            if(j>=AccountLimit):
                break
            if BotScore(reddit.redditor(user),PostLimit) == False:
                correct+=1
            j+=1
    file.close()
    print((100*correct)/(i+j))

print(BotScore('Most-Boring-Bot', 50))
