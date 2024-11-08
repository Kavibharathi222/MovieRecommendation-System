from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import random
import requests

app = Flask(__name__,template_folder="../Frontend", static_folder="../Frontend/static")
CORS(app)  # Enable CORS for all routes

# Load the processed data (make sure your movie data contains the 'tags' column)
with open(r"C:/Users/ripff/Downloads/Movie-Recommendation-System-main/Movie-Recommendation-System-main/movie_data.pkl", 'rb') as file:
    movies, cosine_sim = pickle.load(file)


def get_recommendations_by_tag(tag):
    # Filter movies by tag
    tag_filtered_movies = movies[movies['tags'].str.contains(tag, case=False, na=False)]
    print("CREW",movies)
    if tag_filtered_movies.empty:
        return []
    
    # Select the title and movie_id columns and convert them to a list of tuples
    movie_titles = tag_filtered_movies[['title','overview',]].head(20).to_records(index=False).tolist()
   # movie_ids = [movie[1] for movie in movie_titles]
    # print(movie_titles)
    # print(movie_ids)
    # path =get_movie_image( movie_ids)
    # print(path)
    # Shuffle the movie titles
    random.shuffle(movie_titles)
    
    return movie_titles
    





# Route for the home page
@app.route('/')
def home():
    return render_template("index.html")  # Updated to match the new template

# API endpoint for recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    tag = data.get('tag')
    
    if not tag:
        return jsonify({'error': 'Tag not provided'}), 400
    
    recommendations = get_recommendations_by_tag(tag)
    return jsonify({'recommendations': recommendations})

@app.route('/recommend1')
def recommendations():
    return render_template('recommend.html')
# Route to handle form submission


@app.route('/submit', methods=['POST'])
def submit():
    genre = request.form.get('genre')
    recommendations = get_recommendations_by_tag(genre)
    return render_template('recommendations.html', recommendations=recommendations, genre=genre)

if __name__ == '__main__':
    app.run(debug=True)

















