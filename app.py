from flask import Flask, render_template
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    with open(os.path.join(BASE_DIR, 'data', filename), 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    projects = load_json('projects.json')
    return render_template('projects.html', projects=projects)

@app.route('/reading')
def reading():
    books = load_json('reading.json')
    return render_template('reading.html', books=books)

@app.route('/timeline')
def timeline():
    timeline = load_json('timeline.json')
    return render_template('timeline.html', timeline=timeline)

@app.route('/project')
def project_detail():
    project = {
        'title': 'Sample Project',
        'description': 'More in-depth look at a single project.',
        'image': '',
        'link': 'https://example.com'
    }
    return render_template('project.html', project=project)

if __name__ == '__main__':
    app.run(debug=True)
