import flask

history = flask.Blueprint(
    name= "history" ,
    import_name = "history",
    template_folder= "history/templates",
    static_folder= "history/static"
)