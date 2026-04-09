"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask_wtf.csrf import generate_csrf

from app import app, db
from app.forms import MovieForm
from app.models import Movie
from flask import current_app, jsonify, request, send_from_directory, send_file, render_template
from uuid import uuid4
from werkzeug.utils import secure_filename

import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route("/api/v1/movies", methods=["POST"])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster_file = form.poster.data

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(poster_file.filename)
        unique_filename = f"{uuid4().hex}_{filename}"

        poster_path = os.path.join(upload_folder, unique_filename)
        poster_file.save(poster_path)

        new_movie = Movie(
            title=title,
            description=description,
            poster=unique_filename
        )

        db.session.add(new_movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": new_movie.title,
            "poster": new_movie.poster,
            "description": new_movie.description
        }), 201

    return jsonify({
        "errors": form_errors(form)
    }), 400

@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()

    movies_list = []
    for movie in movies:
        movies_list.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "poster": f"/api/v1/posters/{movie.poster}"
        })

    return jsonify({
        "movies": movies_list
    })
    
@app.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()}) 
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404