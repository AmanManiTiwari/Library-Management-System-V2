from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    MAIL_SERVER='smtp.mailtrap.io',
    MAIL_PORT=2525,
    MAIL_USERNAME='your-mailtrap-username',  # Replace with your Mailtrap username
    MAIL_PASSWORD='your-mailtrap-password',  # Replace with your Mailtrap password
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
)
db = SQLAlchemy(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
mail = Mail(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        title=data['title'], 
        description=data.get('description'), 
        deadline=datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S'), 
        user_id=data['user_id']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'deadline': task.deadline} for task in tasks])

@celery.task
def send_reminder(email, task_title, deadline):
    msg = Message(f"Reminder: {task_title}", recipients=[email])
    msg.body = f"The task '{task_title}' is due by {deadline}. Please complete it on time."
    mail.send(msg)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
