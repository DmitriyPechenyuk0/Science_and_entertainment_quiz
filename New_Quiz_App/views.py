import os, json
from flask import request, render_template, redirect, url_for
from .models import Quiz
from project.settings import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from profile.models import User
import os
import json
from flask import request, jsonify
import string
DIR = os.path.dirname(os.path.abspath(__file__))

@login_required

def render_new_quiz(name):
    if not current_user.is_admin:
        return render_template('error_403.html')
    # print(name)
    print()
    quiz = db.one_or_404(db.select(Quiz).filter_by(name=name))

    context = {
        'page': 'home',
        'is_auth': current_user.is_authenticated,
        'name': current_user.name,
        'quiz': quiz
    }
    return render_template('New_Quiz_App.html', **context)

@login_required
def render_new_quiz_settigs():
    if not current_user.is_admin:
        return render_template('error_403.html')

    if request.method == 'POST':
        try:
            quiz_name = request.form['quiz-name']
            filename = "json_data.json"
            empty_data = []
            
            
            
            file_path = os.path.join(DIR, 'static', 'quiz_data', filename)


            base_media_dir = 'media'
            os.makedirs(base_media_dir, exist_ok=True)

            quiz_folder_in_media = os.path.join(base_media_dir, quiz_name)
            os.makedirs(quiz_folder_in_media, exist_ok=True)

            file_path = os.path.join(quiz_folder_in_media, filename)
            with open(file_path, 'w') as f:
                json.dump(empty_data, f)
            
            image =request.files['image']

            image = request.files.get('image')
            image_filename = None
            if image and image.filename != '':
                image_filename = secure_filename(image.filename)
                media_folder = os.path.join(DIR, 'static', 'media')
                os.makedirs(media_folder, exist_ok=True)
                image_path = os.path.join(media_folder, image_filename)
                image.save(image_path)

            id_user = User.get_id(current_user)

            images_folder_in_media = os.path.join(base_media_dir, 'Images')
            os.makedirs(images_folder_in_media, exist_ok=True)

            quiz = Quiz(
                name=quiz_name,
                json_test_data=os.path.join(base_media_dir, quiz_name, filename),
                count_questions=int(request.form['num-questions']),
                topic=request.form['topic'],
                image=f"{image_filename}" if image_filename else None,
                description=request.form['description'],
                owner = id_user
            )

            db.session.add(quiz)
            db.session.commit()

            return redirect(f'/new-quiz/{quiz_name}')

        except Exception as e:
            print(f"Error while creating quiz: {e}")


    context = {
        'page': 'home',
        'is_auth': current_user.is_authenticated,
        'name': current_user.name
    }
    return render_template('New_Quiz_Settings.html', **context)


@login_required
def render_new_quiz_student():
    context = {
        'page': 'home',
        'is_auth': current_user.is_authenticated,
        'name': current_user.name
    }
    return render_template('New_Quiz_App_Student.html', **context)


@login_required
def render_new_quiz_2_student():
    context = {
        'page': 'home',
        'is_auth': current_user.is_authenticated,
        'name': current_user.name
    }
    return render_template('New_Quiz_App_Student_2.html', **context)


saved_topic = None

@login_required
def save_topic():
    data = request.get_json()
    topic = data.get('topic')

    if topic:
        if any(char in "абвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ" for char in topic):
            language = "Ukrainian"
        elif any(char in string.ascii_letters for char in topic):
            language = "English"
        else:
            language = "Unknown"

        print(f"Received topic: {topic}, Language: {language}")
        return jsonify({"status": "success", "topic": topic, "language": language})
    else:
        return jsonify({"status": "error", "message": "No topic provided"}), 400