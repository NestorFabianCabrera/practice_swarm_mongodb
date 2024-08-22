from flask import Flask, request, redirect, url_for, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongo:27017/mydatabase'
mongo = PyMongo(app)

@app.route('/')
def index():
    items = mongo.db.items.find()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    value = request.form.get('value')
    mongo.db.items.insert_one({'name': name, 'value': value})
    return redirect(url_for('index'))

@app.route('/edit/<item_id>', methods=['POST'])
def edit_item(item_id):
    name = request.form.get('name')
    value = request.form.get('value')
    mongo.db.items.update_one({'_id': ObjectId(item_id)}, {'$set': {'name': name, 'value': value}})
    return redirect(url_for('index'))

@app.route('/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
    mongo.db.items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
