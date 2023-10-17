# 🤖 Reddit Bot Detector
A simple algorithm that uses Reddit's API to identify spam bot accounts.

Different weights are assigned to accounts based on the following heuristics:
Heuristics | Meaning
--- | ---
Account age | Newer accounts are more likely to be flagged as bots.
Karma | Accounts with little karma are more likely to be flagged as bots.
Verified account | Unverified accoounts are more likely to be flagged as bots.
Reddit employee | Accounts are Reddit employees are more likely to be flagged as bots.
Variance in time interval between posts/comments | Accounts posting a lot of comments or posts in a short time interval are more likely to be flagged as bots.
Variance between posts'/comments' content |  Accounts posting a lot of identical comments or posts are more likely to be flagged as bots.

678 different Reddit accounts (bots accounts and non-bots accounts) were used for testing and at most 100 submissions (posts + comments) were analysed for each account. 

> 🔴 **Disclaimer: This program is purely for educational and experimental purposes. It was created to explore the functionalities of Reddit's API and to learn Python programming. It is not designed, tested, or intended for use in any production environment. The author does not assume any responsibility for the program's usage outside of the intended educational context. Users should use the program at their own risk and discretion.**
 
## Usage
- `data.txt` contains a list of Reddit usernames of bots and real people which have been used for testing.
- All the code required is in `main.py`.

Fill the required details for the Reddit instance.
```python
reddit = praw.Reddit(
    client_id="xxxxxxxxx",
    client_secret="xxxxxxxxx",
    user_agent="xxxxxxxxx",
    username = "xxxxxxxxx",
    password = "xxxxxxxxx"
)
```

Call function `BotScore` with a parameter `k` as shown below:
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

The function returns `True` if the user `u/Most-Boring-Bot` is a spam bot.

Algorithm works best when the user has more than 20 posts and comments and when $k > 30$.

## Limitation
- Finding a list of active spam bots is nearly impossible because Reddit bans spam bots automatically. The threshold used for identifying bots is somewhat flawed because my algorithm assumed that my list of bots contains only spam bots. However not all bot accounts are spam bots.

- The accuracy of the program is hard to calculate as well due to lack of data.

## Future work 
### Sample data improvements
- [ ] Remove accounts with less than 100 comments and 100 posts 
- [ ] Remove non-spam bots from list of bots. 
### Heuristics improvements 
- [ ] Check for URL shorteners and whether comments link to the same sites 
- [ ] Check if same links appear in several comments
- [ ] Use better statistical methods to find threshold human/bot
- [ ] Improve algorithm for checking similarity between posts/comments (check word frequency, grammatical mistakes, ...)
