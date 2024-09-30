from celery import Celery
from datetime import timedelta
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

mail = Mail(app)

@celery.task
def send_reminder(email, task_title, deadline):
    msg = Message(f"Reminder: {task_title}", recipients=[email])
    msg.body = f"The task '{task_title}' is due by {deadline}. Please complete it on time."
    mail.send(msg)

# Schedule task reminder
def schedule_reminder(task):
    send_reminder.apply_async((user.email, task.title, task.deadline), countdown=60*60*24)  # 1 day reminder
