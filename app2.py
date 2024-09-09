from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

app = Flask(__name__)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=dfcb8704d18c9bbde0c3180585b8eaff"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/150"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:9]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Load data
movies_dict = pickle.load(open('E:\\ANU Projects\\Movie-Recommendation-System\\picklefile\\movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('E:\\ANU Projects\\Movie-Recommendation-System\\picklefile\\similarity.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].values
    if request.method == 'POST':
        selected_movie = request.form['selected_movie']
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        return render_template('index.html', movie_list=movie_list, recommendations=zip(recommended_movie_names, recommended_movie_posters))
    return render_template('index.html', movie_list=movie_list, recommendations=None)

if __name__ == '__main__':
    app.run(debug=True)
