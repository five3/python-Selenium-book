from flask import Flask
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'apiman'
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    active_user = mongo.db.users.find({'status': 'active'})
    return json.dumps(active_user)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)

