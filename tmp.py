from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from sklearn.ensemble import IsolationForest

clf = IsolationForest()
clf.decision_function()

print(word_tokenize('change.'))