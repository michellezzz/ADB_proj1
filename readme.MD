#Project 1
http://www.cs.columbia.edu/~gravano/cs6111/proj1.html

---------------
###Team member: 
Moning Zhang(mz2499)
Xingying Liu(xl2493)

----------------
###List of file

bing.py (main file)
document.py 
Rocchio.py  (algorithm)
stop.rtf (stopword list)
stemming (folder)
run_result.txt (run transcript)

----------------
###How to run:

In terminal: python bing.py <precision> <query>
example: python bing.py 0.9 gates

----------------
###Key:
Your key

----------------
###Code description:

The main algorithm for query extension is the Rocchio's algorithm. And the score we used is the tf-idf weighting.
score[doc][word] = log(TF(w,d)+1)*log(IDF(w))

In each iteration, we add only one new word with the highest score to the query as the new query. 

To make the order of the new query reasonable, we evaluate each permutation of the new query by the bi-gram frequency model. i.e, For each permutation of the query, we sum up its all bigram-term’s term frequency as score.

For the core algorithm, we gather the word statistical information from both the title and description fields. To make our program more feasible, we add two additional parameters to control the weight of different fields. 
You can change these parameters on line 124 and 125 in the Rocchio.py

