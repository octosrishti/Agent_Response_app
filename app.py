from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    message_content = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=True)
    agent_name = db.Column(db.String(100), nullable=True)

def init_db():
    """Initialize the database and load messages from CSV."""
    with app.app_context():
        db.create_all()
        if not Message.query.first():
            load_messages_from_csv('messages.csv')

import os

def load_messages_from_csv(filename):
    """Load messages from a CSV file into the database."""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            message = Message(
                user_id=row['user_id'],
                timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'),
                message_content=row['message_body']
            )
            db.session.add(message)
        db.session.commit()

@app.route('/')
def index():
    """Display all messages."""
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/respond/<int:message_id>', methods=['POST'])
def respond(message_id):
    """Handle agent responses to messages."""
    response = request.form['response']
    agent_name = request.form['agent_name']

    message = Message.query.get(message_id)
    message.response = response
    message.agent_name = agent_name
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
