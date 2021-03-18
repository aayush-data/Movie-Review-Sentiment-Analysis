import urllib2 
from wordcloud import WordCloud 
from bs4 import BeautifulSoup 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from nltk.tokenize import RegexpTokenizer 
from nltk.stem import WordNetLemmatizer 
import nltk 

reviews = [] 
ranking_scored = [] 


def get_reviews(movie_id, pages):
	for i in range(1, int(pages)+1, 1):
		loop_url = url+"?page="+str(i)
		loop_review_page = urllib2.urlopen(loop_url)
		loop_soup = BeautifulSoup(loop_review_page, "html.parser")

		for x in loop_soup.find_all("div", attrs = {"class": "review_desc"}):
			for y in x.find_all("div", attrs = {"class": "the_review"}):
				review = y.get_text()
			for z in x.find_all("div", attrs = {"class": "small subtle"}):
				rate = z.get_text().strip().split()[-1]
				if rate == "Review":
					rate = np.nan
				else:
					pass

			reviews.append([review, rate])

def ranked_reviews(movie_id, pages):
    global rate
    rank_dict = {"A+": 1, "A": 0.96, "A-": 0.92, "B+": 0.89, "B": 0.86, "B-": 0.82, "C+": 0.79, "C": 0.76, "C-": 0.72, "D+": 0.69, "D": 0.66, "D-": 0.62}
    for review, rate in reviews:
    	if rate == np.nan: 
    		pass
    	elif type(rate) != float and rate[0] in rank_dict.keys(): 
    		norm_rate = rank_dict[rate[0]]
        elif str(rate).isalpha() == True: 
            continue
    	elif rate != np.nan: 
    		rate = str(rate).split("/")
    		try:
    			norm_rate = float(rate[0]) / float(rate[1])
    		except: # To avoid errors if the scale isn't mentioned
    			norm_rate = float(rate[0]) / 10.0
		ranking_scored.append([review, norm_rate])
    print "\n\nAuthor: ", pages

movie_id = raw_input("Enter the name of Movie you want to see the reviews of: ") # Asking user for a movie
url = "https://www.rottentomatoes.com/m/"+movie_id+"/reviews/" # Setting the url as per the link on rotten tomatoes
print "\nGathering page info for", movie_id # User confirmation print if error occurs the movie_id is incorrect
name = "Aayush Garg" # Author name

# Import the page
homepage = urllib2.urlopen(url) # Passing the movie_id in url and opening the link in python

# Creating soup
soup = BeautifulSoup(homepage, "html.parser") # Getting the whole page data

# Help link -> https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
pages = soup.find("span", attrs = {"class": "pageInfo"}) # Getting the total pages of critic's reviews
pages = pages.get_text().strip().split()[-1] # Getting the exact value of pages
#print pages
print "\nReviws are divided in", pages, "pages"

get_reviews(movie_id, pages) # Getting movie reviews from HTML page
ranked_reviews(movie_id, name) # Sorting the reviews
# For sorting and storing values in a pandas datastructure, for future use
df = pd.DataFrame(ranking_scored) 
df.columns = ["Review","Rating"]
df = df.sort_values("Rating", ascending = True).dropna()

# Storing top/bottom values and other values for data word cloud
top_ = df.tail(20)
top_20 = df.tail(80)
bottom_ = df.head(20)
bottom_20 = df.head(80)

# Printing top/bottom 20 reviews
print "\nTop 20 reviews are\n", top_
print "\n\nBottom 20 reviews are\n", bottom_

top_20_text = []
bottom_20_text = []
top_20_tok = []
bottom_20_tok = []
cleaned_top = []
cleaned_bottom = []

# cleaning loops start
for i in top_20["Review"].astype("str"):
    i = i.lower().strip().split()
    for words in i:
        top_20_text.append(words)
        
for i in bottom_20["Review"].astype("str"):
    i = i.lower().strip().split()
    for words in i:
        bottom_20_text.append(words)

control = open("stopwords_en.txt", "r")
control = control.read().lower()
    
        
tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()

stop = control.replace("\n", " ")
stop = tokenizer.tokenize(stop)
# Adding the obvious occurances to stopwords to be removed from word cloud
stop.append("incredibles")
stop.append("film")
stop.append("movie")

for tok in top_20_text:
    tok = tokenizer.tokenize(tok)
    tok = "".join(tok)
    lem = lemmatizer.lemmatize(tok)
    top_20_tok.append(str(lem))
    
for tok2 in bottom_20_text:
    tok2 = tokenizer.tokenize(tok2)
    tok2 = "".join(tok2)
    lem2 = lemmatizer.lemmatize(tok2)
    bottom_20_tok.append(str(lem2))
    
for i in top_20_tok:
	if i.isalpha() and i not in stop:
		cleaned_top.append(i)
        
for j in bottom_20_tok:
	if j.isalpha() and j not in stop:
		cleaned_bottom.append(j)
# Cleaning loops end
        
# for word cloud
cleaned_top_join = " ".join(cleaned_top)
cleaned_bottom_join = " ".join(cleaned_bottom)
stop = " ".join(stop)

wc = WordCloud(stopwords = stop, background_color = "white").generate(cleaned_top_join)
plt.figure()
plt.imshow(wc)
plt.axis("off")
plt.title("Wordcloud of Top 20\n\n")
plt.show()

wc2 = WordCloud(stopwords = stop, background_color = "white").generate(cleaned_bottom_join)
plt.figure()
plt.imshow(wc2)
plt.axis("off")
plt.title("Wordcloud of Bottom 20\n\n")
plt.show()

# Making bigrams using nltk package
for_biag = list(nltk.bigrams(cleaned_top + cleaned_bottom))
print "Top 10 biagrams are:\n"
for i in range(1,11,1):
    print for_biag[i]
