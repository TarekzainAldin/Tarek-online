from falsk import Flask


def create_app():
  app =Flask(__name__)
  app.config['SECRET_KEY']='TAREK ZAIN ALDIN'

  return app
