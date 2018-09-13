from sklearn import datasets
boston = datasets.load_boston()

# Shuffle the data
from sklearn.utils import shuffle
data, target = shuffle(boston.data, boston.target, random_state=0)
