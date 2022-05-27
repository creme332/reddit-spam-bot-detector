# 🤖Basic spam bot detection algorithm
An algorithm that identifies spam bots with 40-50 %* accuracy. 

>⚠️ $Disclaimer$
>
> 678 different Reddit accounts (bots accounts and non-bots accounts) were used for testing. At most 100 submissions (posts+comments) were analysed for each account. Finding a list of active spam bots is nearly impossible because Reddit bans most spam bots automatically. My algorithm assumed that the list of bots contains spam bots only so the presence of non-spam bots significantly reduced its accuracy. 

This code was written for fun to experiment with PRAW and must not be taken seriously. 
# 🚀Setup #

1. All the code required is in `main.py`.

1. Fill the required details for the Reddit instance.
```python
reddit = praw.Reddit(
    client_id="xxxxxxxxx",
    client_secret="xxxxxxxxx",
    user_agent="xxxxxxxxx",
    username = "xxxxxxxxx",
    password = "xxxxxxxxx"
)
```
1. Call function `BotScore` as shown below :

```python
print(BotScore('Most-Boring-Bot', k)) 
# k : number of posts to be analysed. 0 < k < 1000
```
Output :
```
115.44958793954774
True
```
The first number is indicates the likelihood of being a spam bot. (the higher the number the more likely)

The function returns True if the user `u/Most-Boring-Bot` is a spam bot.

Algorithm works best when the user has more than 20 posts/comments and when $k > 30$

`data.txt` contains a list of Reddit usernames of bots and real people which have been used for testing.

# 🛰️Heuristics #
Heuristics 
--- | 
Account age and karma
Verified account
Reddit employee 
Variance in time interval between posts/comments 
Variance between posts'/comments' content 

# 🔮Future work #
### Sample data improvements ###
- [ ] Remove accounts with less than 100 comments and 100 posts 
- [ ] Remove non-spam bots from list of bots. 
### Heuristics improvements ###
- [ ] Check for URL shorteners and whether comments link to the same sites 
- [ ] Check if same links appear in several comments
- [ ] Use better statistical methods to find threshold human/bot
- [ ] Improve algorithm for checking similarity between posts/comments (check word frequency, grammatical mistakes, ...)
