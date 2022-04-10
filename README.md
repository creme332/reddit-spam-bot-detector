# Basic spam bot detection algorithm
An algorithm that identifies bots (mainly spam bots) with 70%* accuracy.
This code was written for fun to experiment with Python.

\*  60 submissions and comments from 678 different Reddit accounts were used for testing

# How to use #

Fill in the required details for the Reddit instance

Call function

```python
print(FinalReport('Most-Boring-Bot', k)) 
# k : number of posts to be analysed. 0 < k < 1000
```
The function returns 1 if the user `u/Most-Boring-Bot` is a spam bot.

Algorithm works best when the user has more than 20 posts and more than 20 comments and when k > 30 
# Heuristics #
Heuristics 
--- | 
Account age and karma
Verified account
Reddit employee 
Variance in time interval between posts/comments 
Variance between posts'/comments' content 
# Current limitations #
- Algorithm cannot not differentiate between a bot and a spam bot.
# Future work #
- [ ] Check for URL shorteners and whether comments link to the same sites 
- [ ] Check if same links appear in several comments
- [ ] Remove non-spam bots from list of bots
- [ ] Use better statistical methods to find threshold human/bot
- [ ] Increase number of posts analysed per account
- [ ] Improve algorithm for checking similarity between posts/comments (check word frequency, grammatical mistakes, ...)
