import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# creating dfb
df = pd.read_csv('final.csv')

# notna function maps exisitng elements with true and non exisiting elements to false
# this operation removes rows mapped to false
df = df[df['soup'].notna()]

# creating matix / vector
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df['soup'])

# similarity object : classifier
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# resetting index of dataframe
df = df.reset_index()
indices = pd.Series(df.index, index = df['original_title'])

def get_recommendations(title):
   idx = indices[title]
   sim_scores = list(enumerate(cosine_sim2[idx]))
   sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
   sim_scores = sim_scores[1:11]
   movie_indices = [i[0] for i in sim_scores]

   return df[['original_title','poster_link','runtime','release_date','weighted_rating']].iloc[movie_indices]

