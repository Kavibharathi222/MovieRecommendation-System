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

# Function to get genre/tag-based recommendations
import random


api_token = 'd59a3d8149b828a4fd4ef68f2045cc61'

# Function to get movie ID from title
def get_movie_id(title):
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_token}&query={title}'
    response = requests.get(search_url)
    data = response.json()
    
    if data['results']:
        return data['results'][0]['id']  # Return the first result's ID
    return None

def get_movie_image(movie_id):
    movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_token}'
    response = requests.get(movie_url)
    data = response.json()
    
    # Base URL for images
    image_base_url = 'https://image.tmdb.org/t/p/w500'  # You can change 'w500' to other sizes
    poster_path = data.get('poster_path')
    
    if poster_path:
        return f'{image_base_url}{poster_path}'
    return None

def get_recommendations_by_tag(tag):
    # Filter movies by tag
    tag_filtered_movies = movies[movies['tags'].str.contains(tag, case=False, na=False)]
    print("CREW",movies)
    if tag_filtered_movies.empty:
        return []
    
    # Select the title and movie_id columns and convert them to a list of tuples
    movie_titles = tag_filtered_movies[['title','overview',]].head(20).to_records(index=False).tolist()
    movie_ids = [movie[1] for movie in movie_titles]
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

















# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# import pickle
# import pandas as pd
# import random
# import requests

# app = Flask(__name__, template_folder="../Frontend", static_folder="../Frontend/static")
# CORS(app)

# # Load the processed data
# with open(r"C:/Users/ripff/Downloads/Movie-Recommendation-System-main/Movie-Recommendation-System-main/movie_data.pkl", 'rb') as file:
#     movies, cosine_sim = pickle.load(file)

# api_token = 'd59a3d8149b828a4fd4ef68f2045cc61'

# # Function to get movie ID from title
# def get_movie_id(title):
#     search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_token}&query={title}'
#     try:
#         response = requests.get(search_url)
#         response.raise_for_status()  # Raise an error for bad responses
#         data = response.json()
#         if data['results']:
#             return data['results'][0]['id']
#     except requests.exceptions.RequestException as e:
#         print(f"Error getting movie ID for '{title}': {e}")
#     return None

# # Function to get movie image URL
# def get_movie_image(movie_id):
#     movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_token}'
#     try:
#         response = requests.get(movie_url)
#         response.raise_for_status()
#         data = response.json()
#         image_base_url = 'https://image.tmdb.org/t/p/w500'
#         poster_path = data.get('poster_path')
#         return f'{image_base_url}{poster_path}' if poster_path else None
#     except requests.exceptions.RequestException as e:
#         print(f"Error getting image for movie ID '{movie_id}': {e}")
#         return None

# # Function to get recommendations by tag
# def get_recommendations_by_tag(tag):
#     tag_filtered_movies = movies[movies['tags'].str.contains(tag, case=False, na=False)]
    
#     if tag_filtered_movies.empty:
#         return []  # No movies found
    
#     movie_titles = tag_filtered_movies[['title']].head(20)['title'].tolist()
#     random.shuffle(movie_titles)
    
#     movie_info_list = []
#     for title in movie_titles:
#         movie_id = get_movie_id(title)
#         image_url = get_movie_image(movie_id) if movie_id else None
#         movie_info_list.append({'title': title, 'image_url': image_url})

#     return movie_info_list  # Return list instead of render_template

# # Route for the home page
# @app.route('/')
# def home():
#     return render_template("index.html")

# # API endpoint for recommendations
# @app.route('/recommend', methods=['POST'])
# def recommend():
#     data = request.json
#     tag = data.get('tag')
    
#     if not tag:
#         return jsonify({'error': 'Tag not provided'}), 400
    
#     recommendations = get_recommendations_by_tag(tag)
#     return jsonify({'recommendations': recommendations})

# # Route to handle form submission
# @app.route('/submit', methods=['POST'])
# def submit():
#     genre = request.form.get('genre')
#     recommendations = get_recommendations_by_tag(genre)
#     return render_template('recommendations.html', recommendations=recommendations, genre=genre)

# if __name__ == '__main__':
#     app.run(debug=True)
