from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'apiman'
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testing', methods=['POST'])
def testing():
    return ""

@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)

