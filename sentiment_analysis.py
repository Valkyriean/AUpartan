# only first time
import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
text = '''
After a few covid delays I finally got to graduate last night! So grateful for my amazing supervisors and my lab, it’s been a journey but I made it!
Not anymore and hopefully not again
Not anymore and hopefully not again #lockdown #covid #corona #fitzroy #graffiti #slogangraffiti @graffiterati @sevenbreaths
Novak’s antivac supporters. Novak contracted Covid for the 2nd time in Dec 2021 and still refused vaccination. What is wrong with your brain, dude? Get vaccinated!

'''

res = sia.polarity_scores(text)

print(res)