import flask, os

DIR = os.path.dirname(os.path.abspath(__file__))

New_Quiz = flask.Blueprint(
  name = "New_Quiz",
  import_name = "New_Quiz_App",
  template_folder = "templates",
  static_folder = os.path.join(DIR, 'static'),
  static_url_path= "/new_quiz",
)



