from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/map/')
def map():
    return render_template('map.html')