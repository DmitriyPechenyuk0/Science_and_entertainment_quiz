import home_app, New_Quiz_App

from .settings import project


home_app.home.add_url_rule(rule= '/', view_func=home_app.show_home_page, methods = ['POST', 'GET'])

New_Quiz_App.New_Quiz.add_url_rule(rule= '/new-quiz', view_func=New_Quiz_App.render_new_quiz, methods = ['POST', 'GET'])
New_Quiz_App.New_Quiz.add_url_rule(rule= '/new-quiz-2', view_func=New_Quiz_App.render_new_quiz_2, methods = ['POST', 'GET'])

project.register_blueprint(blueprint=home_app.home)

project.register_blueprint(blueprint=New_Quiz_App.New_Quiz)

