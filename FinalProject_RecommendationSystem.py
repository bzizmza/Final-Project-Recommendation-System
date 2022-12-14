# -*- coding: utf-8 -*-
"""FinalProject_RecommendationSystem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zp24VBOyooU5Gw40-4DkiyHISFoRDflg

# Final Project: Recommendation System
**by Abimanyu Sri Setyo**

**About Project**<br>
During the last few decades, with the rise of Youtube, Amazon, Netflix and many other such web services, recommender systems have taken more and more place in our lives. From e-commerce to online advertisement, recommender systems are today unavoidable in our daily online journeys. In a very general way, recommender systems are algorithms aimed at suggesting relevant items to users. Recommender systems are really critical in some industries as they can generate a huge amount of income when they are efficient or also be a way to stand out significantly from competitors.

**About Dataset**<br>
The dataset is publically available on the [Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset) website, and collected by Cai-Nicolas Ziegler in a 4-week crawl (August / September 2004) from the Book-Crossing community with kind permission from Ron Hornbaker, CTO of Humankind Systems. Contains 278,858 users (anonymized but with demographic information) providing 1,149,780 ratings (explicit / implicit) about 271,379 books.

## Table of Contents

>[Final Project: Recommendation System](#scrollTo=wSn1cZsah1Sg)

>>[Table of Contents](#scrollTo=a00X1YD1mmu0)

>>[Data Loading](#scrollTo=h_fkpGsmhyWJ)

>>>[Import Libraries](#scrollTo=GBCcJqAincC0)

>>>[Import Dataset](#scrollTo=DfhQs3pPngkl)

>>[Exploratory Data Analysis](#scrollTo=PQXGQLlaiDnx)

>>>[Variable Description](#scrollTo=QSkcf-KDupGT)

>>>[Drop unneeded data](#scrollTo=LmO9s8iriqnA)

>>>[Handle missing and duplicates values](#scrollTo=_sEd_hs0x1d-)

>>>[Fixed header name](#scrollTo=ZRIN9J-uvwBS)

>>>[Univariate Data Analysis](#scrollTo=98p06kaft_me)

>>>[Multivariate Data Analysis](#scrollTo=2dH-Z6q3APVt)

>>[Model Development with Content Based Filtering](#scrollTo=d3JWEQ39k82r)

>>[Model Development with Collaborative Filtered](#scrollTo=TBgo2k63Ek-r)

## Data Loading
Preparing the dataset for use

### Import Libraries
Import the required libraries
"""

import zipfile

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow import keras
from tensorflow.keras import layers

"""### Import Dataset
Importing datasets, here the datasets used are sourced from [Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset), so installation of the [Kaggle library](https://pypi.org/project/kaggle/) is required.
"""

! pip install kaggle

! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets download arashnic/book-recommendation-dataset

local_zip = '/content/book-recommendation-dataset.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content/book-recommendation')
zip_ref.close()

# Commented out IPython magic to ensure Python compatibility.
# %cd book-recommendation
# %ls

books = pd.read_csv('/content/book-recommendation/Books.csv')
ratings = pd.read_csv('/content/book-recommendation/Ratings.csv')

"""## Exploratory Data Analysis
Quoted from [algorit.ma](https://algorit.ma/blog/exploratory-data-analysis-2022/), Exploratory Data Analysis covers the critical process of preliminary investigation tests on data to identify patterns, find anomalies, test hypotheses, and check assumptions through summary statistics and graphical (visual) representations.

### Variable Description
Take an in-depth look at what's interesting to see in the dataset.
"""

books.head()

ratings.head()

print(ratings.shape)
print(books.shape)

"""### Drop unneeded data
Judging from the dataframe of the rating and books, there are quite a lot, here I only take 10000 rows from the book dataset and 5000 rows for the rating dataset
"""

books = books[:10000]
ratings = ratings[:5000]

"""### Handle missing and duplicates values
According to [DQLab.id](https://www.dqlab.id/kursus-belajar-data-mengenal-apa-itu-missing-value), missing values will make the data unusable, and it's a shame to throw away important information in many rows just because of 1-2 missing values, so one of the right steps is to fill in the missing values.
"""

# Check NaN values
print ("Sum of\t->\tColumn")
print ("Values")
print ("=======================")
for i in books.columns:
    print (str(books[i].isna().sum()) + "\t->\t" + i)

# Check NaN values
print ("Sum of\t->\tColumn")
print ("Values")
print ("=======================")
for i in ratings.columns:
    print (str(ratings[i].isna().sum()) + "\t->\t" + i)

books = books.dropna()
ratings = ratings.dropna()

ratings = ratings.drop_duplicates()
books = books.drop_duplicates()

"""### Fixed header name"""

ratings.head()

ratings = ratings.rename(columns={'Book-Rating': 'rating','User-ID':'user_id'})
ratings.head()

books.head()

books = books.rename(columns={'Book-Title': 'book_title','Book-Author':'book_author','Year-Of-Publication':'year_of_publication','Image-URL-S':'Image_URL_S','Image-URL-M':'Image_URL_M','Image-URL-L':'Image_URL_L'})
books.head()

ratings[ratings.rating == max(ratings.rating)]
best_booksId = ratings.ISBN[ratings.rating == max(ratings.rating)]
best_booksId = list(dict.fromkeys(best_booksId))

"""### Univariate Data Analysis
Sourced from the [SanberCode Blog](https://blog.sanbercode.com/docs/materi-eda/univariate-bivariate-multivariate-analysis/), Univariate Analysis is a technique for understanding and exploring data. The prefix 'Uni' means 'one', so univariate analysis is a single feature data analysis.
"""

ratings.head()

count = ratings["rating"].value_counts()
count.plot(kind='bar', title="Rating");
 
plt.show()

books.head()

count = books["year_of_publication"].value_counts()
count.plot(kind='bar', title="Year of Publication");
 
plt.show()

"""### Multivariate Data Analysis"""

sns.pairplot(ratings, diag_kind = 'kde')

"""## Model Development with Content Based Filtering"""

books.shape

ratings.shape

books.head()

"""Convert Books dataframe to List"""

book_ISBN = books['ISBN'].tolist()
book_title = books['book_title'].tolist()
book_author = books['book_author'].tolist()
book_year_of_publication = books['year_of_publication'].tolist()

book = pd.DataFrame({
    'book_ISBN': book_ISBN,
    'book_title': book_title,
    'book_author': book_author,
    'book_year_of_publication': book_year_of_publication
})
book

"""Get the book author"""

tf = TfidfVectorizer()
tf.fit(book['book_author']) 
tf.get_feature_names()

"""Do fit and transform into matrix"""

tfidf_matrix = tf.fit_transform(book['book_author']) 
tfidf_matrix.shape

tfidf_matrix.todense()

pd.DataFrame(
    tfidf_matrix.todense(), 
    columns=tf.get_feature_names(),
    index=book.book_title
).sample(10, axis=1,replace=True).sample(10, axis=0)

"""In the recommendation system, we need to find a way so that the items we recommend are not too far from the central data, therefore we need the degree of similarity on the items, in this project, books with the degree of similarity between books with cosine similarity"""

cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim

cosine_sim_df = pd.DataFrame(cosine_sim, index=book['book_title'], columns=book['book_title'])

def author_recommendations(i, M, items, k=5):
    ix = M.loc[:,i].to_numpy().argpartition(range(-1,-k,-1))
    closest = M.columns[ix[-1:-(k+2):-1]]
    closest = closest.drop(i, errors='ignore')
    return pd.DataFrame(closest).merge(items).head(k)

"""Test book using title "Adventures of Huckleberry Finn (Dover Thrift Editions)"
"""

books_that_have_been_read = "Adventures of Huckleberry Finn (Dover Thrift Editions)"
book[book.book_title.eq(books_that_have_been_read)]

recommendations = author_recommendations(books_that_have_been_read, cosine_sim_df, book[['book_title', 'book_author']])

recommendations = recommendations.drop_duplicates()

"""Featuring 5 recommended books written by the same author."""

recommendations

books_that_have_been_read_row = books[books.book_title == books_that_have_been_read]
books_that_have_been_read_author = books_that_have_been_read_row.iloc[0]["book_author"]

book_recommendation_authors = recommendations.book_author

real_author = 0
for i in range(5):
    if book_recommendation_authors[i] == books_that_have_been_read_author:
        real_author+=1

Accuracy = real_author/5*100
print("Accuracy of the model is {}%".format(Accuracy))

"""## Model Development with Collaborative Filtered

Convert user_id to integer
"""

user_ids = ratings['user_id'].unique().tolist()
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}

"""Convert book_id to integer"""

book_ids = ratings['ISBN'].unique().tolist()
book_to_book_encoded = {x: i for i, x in enumerate(book_ids)}
book_encoded_to_book = {i: x for i, x in enumerate(book_ids)}

ratings['user'] = ratings['user_id'].map(user_to_user_encoded)
ratings['book'] = ratings['ISBN'].map(book_to_book_encoded)

"""Check total users and books"""

num_users = len(user_encoded_to_user)
print(num_users)
num_book = len(book_encoded_to_book)
print(num_book)

"""Convert ratings to float"""

ratings['rating'] = ratings['rating'].values.astype(np.float32)

min_rating = min(ratings['rating'])
max_rating = max(ratings['rating'])
 
print('Number of User: {}, Number of Book: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_book, min_rating, max_rating
))

"""Split the dataset into train data and validation data"""

ratings = ratings.sample(frac=1, random_state=42)
ratings

x = ratings[['user', 'book']].values
 
y = ratings['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
 
train_indices = int(0.70 * ratings.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)
 
print(x, y)

"""Training the Model"""

import tensorflow as tf

class RecommenderNet(tf.keras.Model):
 
  def __init__(self, num_users, num_book, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_book = num_book
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding(
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1)
    self.book_embedding = layers.Embedding( 
        num_book,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.book_bias = layers.Embedding(num_book, 1) 
 
  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0])
    user_bias = self.user_bias(inputs[:, 0])
    book_vector = self.book_embedding(inputs[:, 1])
    book_bias = self.book_bias(inputs[:, 1]) 
 
    dot_user_book = tf.tensordot(user_vector, book_vector, 2) 
 
    x = dot_user_book + user_bias + book_bias
    
    return tf.nn.sigmoid(x)

model = RecommenderNet(num_users, num_book, 50)

model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 5,
    epochs = 20,
    validation_data = (x_val, y_val),
)

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""Get Recommendation"""

books =  book
ratings = ratings

user_id = ratings.user_id.sample(1).iloc[0]
books_have_been_read_by_user = ratings[ratings.user_id == user_id]
 
books_have_not_been_read_by_user = books[books['book_ISBN'].isin(books_have_been_read_by_user.ISBN.values)]['book_ISBN'] 
books_have_not_been_read_by_user = list(
    set(books_have_not_been_read_by_user)
    .intersection(set(book_to_book_encoded.keys()))
)
 
books_have_not_been_read_by_user = [[book_to_book_encoded.get(x)] for x in books_have_not_been_read_by_user]
user_encoder = user_to_user_encoded.get(user_id)
user_book_array = np.hstack(
    ([[user_encoder]] * len(books_have_not_been_read_by_user), books_have_not_been_read_by_user)
)

ratings = model.predict(user_book_array).flatten()
 
top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_book_ids = [
    book_encoded_to_book.get(books_have_not_been_read_by_user[x][0]) for x in top_ratings_indices
]
 
top_books_recommended = (
    books_have_been_read_by_user.sort_values(
        by = 'rating',
        ascending=False
    )
    .head(5)
    .ISBN.values
)
 
books_row = books[books['book_ISBN'].isin(top_books_recommended)]
for row in books_row.itertuples():
    print(row.book_title, 'by', row.book_author)
 
print('----' * 8)
print('Top 10 Book Recommendation for user: {}'.format(user_id))
print('----' * 8)
 
recommended_books = books[books['book_ISBN'].isin(recommended_book_ids)]
for row in recommended_books.itertuples():
    print(row.book_title,'by', row.book_author)