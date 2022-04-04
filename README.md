# SpamBotDetection
A basic bot that identifies spam bots on Reddit with 90% certainty.

# Heuristics #
Heuristics | Weight 
--- | --- 
Account is relatively new | 20
Account has no verified email|  50
Reddit employee | -30
Uses generic name | 40
Time interval between posts/comments | variance * 10
Number of identical posts/comments | % of identical comments
Number of downvotes in comments | 
Posts/comments contain similar phrasing |
Posts/comments links to the same sites | 50
Make the same grammar mistakes| 30
Posts contains URL shorteners | 30
