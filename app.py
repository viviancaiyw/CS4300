from app import app, socketio, db
from app.accounts.models.user import User
import click

@click.command()
@click.option('--port', default=5000, prompt='port to use', help='The port to use for the app')
def init(port):
  print("Flask app running at http://0.0.0.0:{}".format(port))
  socketio.run(app, host="0.0.0.0", port=port)

@app.shell_context_processor
def make_shell_context():
  return {'db':db, 'User':User}

if __name__ == "__main__":
  init()

