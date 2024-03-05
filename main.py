from flask import Flask, jsonify
import pandas as pd
from content_filtering import get_recommendations
from demographic_filtering import output


movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

# extracting important information from dataframe
all_movies=movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

# variables to store data
liked_movies=[]
not_liked_movies=[]
did_not_watch=[]

# method to fetch data from database
def assign_val():
  m_data={
    "original_title": all_movies.iloc[0,0], "poster_link": all_movies.iloc[0,1], "release_date": all_movies.iloc[0,2] or "N/A", "duration": all_movies.iloc[0,3], "rating":all_movies.iloc[0,4]/2
  }
  return m_data
# /movies api
@app.route("/movies")
def get_movies():
  movie_data=assign_val()
  return jsonify({
    "data":movie_data,
    "status":"success"

  })
# /like api
@app.route("/like")
def like():
  global liked_movies
  return jsonify({
    "data":liked_movies,
    "status":"success"
  })

# /dislike api
@app.route("/dislike")
def unliked_movie():
  global all_movies
  movies_data=assign_val()
  not_liked_movies.append(movies_data)
  all_movies.drop([0],inplace=True)
  all_movies=all_movies.reset_index(drop=True)
  return jsonify({
    "status":"success"

  })


# /did_not_watch api
@app.route("/did_not_watch")
def did_not_watch_view():
  global all_movies
  movie_data=assign_val()
  did_not_watch.append(movie_data)
  all_movies.drop([0],inplace=True)
  all_movies=all_movies.reset_index(drop=True)
  return jsonify({
    "status":"success"

  })

@app.route("/popular_movies")
def popular_movies():
  popular_movie_data=[]
  for index,row in output.iterrows():
    p={"original_title": row['original_title'], "poster_link":row['poster_link'], "release_date":row['release_date'] or "N/A", "duration": row['runtime'], "rating": row['weighted_rating']/2}
    popular_movie_data.append(p)
  return jsonify({
    "data":popular_movie_data,
    "status":"success"
  })

@app.route("/recommended_movies")
def recommended_movies():
  global liked_movies
  column_names=["original_title","poster_link","release_date","runtime","weighted_rating"]
  all_recommended=pd.DataFrame(columns=column_names)
  for movie in liked_movies:
    output=get_recommendations(movie["original_title"])
    all_recommended=all_recommended.append(output)
  all_recommended.drop_duplicates(subset=["original_title"],inplace=True)
  recommended_movies_data=[]
  for index,row in all_recommended.iterrows():
    p={"original_title": row['original_title'], "poster_link":row['poster_link'], "release_date":row['release_date'] or "N/A", "duration": row['runtime'], "rating": row['weighted_rating']/2}
    recommended_movies_data.append(p)
  return jsonify({
    "data":recommended_movies_data,
    "status":"success"
  })

if __name__ == "__main__":
  app.run()
