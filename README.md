# Basic bot detection algorithm
An algorithm that identifies bots (mainly spam bots) with % accuracy. 12,000 posts from 600+ Reddit accounts were used to reach this level of accuracy.

This code was written for fun to experiment with Python.


# How to use #

Fill in the required details for the Reddit instance

Call function

```python
print(FinalReport('Most-Boring-Bot', k)) 
# k : number of posts to be analysed. 0 < k < 1000
```
The function returns 1 if the user `u/Most-Boring-Bot` is a bot.

Algorithm works best when the user has more than 20 posts/comments.
# Heuristics #
Heuristics 
--- | 
Account age and karma
Verified account
Reddit employee 
Variance in time interval between posts/comments 
Variance between posts'/comments' content 

# Future work #
- [ ] Check for URL shorteners and whether comments link to the same sites 
- [ ] Check if same links appear in several comments
- [ ] Use better statistical methods to find threshold human/bot
- [ ] Increase number of posts analysed per account
- [ ] Improve algorithm for checking similarity between posts/comments (check word frequency, grammatical mistakes, ...)
