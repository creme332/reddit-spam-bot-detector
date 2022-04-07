# Bot detection algorithm
An **extremely** basic bot that identifies bots or spam bots on Reddit with 60% accuracy on a small sample.

This code was written for fun to experiment with Python.


# How to use #
```python
print(FinalReport('Most-Boring-Bot', k)) 
# k : number of posts to be analysed. 0 < k < 1000
```
The function returns 1 if the user `u/Most-Boring-Bot` is a bot.
# Heuristics #
Heuristics 
--- | 
Account age and karma
Verified account
Reddit employee 
Variance in time interval between posts/comments 
Variance between posts/comments content 

# Future work #
- [ ] Heuristic : Check for URL shorteners in post and whether comments link to the same sites 
- [ ] Use statistics to find threshold for totalscore
- [ ] Increase testing sample size
- [ ] Improve algorithm for checking similarity between posts/comments
