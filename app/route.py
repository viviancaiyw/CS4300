from app import app
from flask import render_template

@app.route('/')
@app.index('/index')
def index():
    return render_template('index.html')