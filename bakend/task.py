from workers import celery
from models import *
from mailer import send_email
from datetime import datetime, timedelta
from flask import render_template 
from celery.schedules import crontab
from flask_mail import Mail, Message
import os
import csv

# @celery.task
# def add():
#     a=1
#     b=2
#     return a+b

# @celery.task
# def multiply(a,b):
    
#     return a*b



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/1"), daily_reminder.s(), name="every day reminder (every minute)")
    #sender.add_periodic_task(crontab(hour=8, minute=0), daily_reminder.s(), name="every day reminder (every day at 8 AM)")
    sender.add_periodic_task(crontab(minute="*/1"), monthly_report.s(), name="monthly report (every min)")
    #sender.add_periodic_task(crontab(hour=7, minute=0, day_of_month="1"), monthly_report.s(), name="monthly report (every month)")
    




@celery.task
def daily_reminder():
    # one_minute_ago = datetime.now() - timedelta(minutes=1)
    # inactive_users = User.query.filter(User.latest_loggedin < one_minute_ago).filter(User.is_librarian == False).all()

    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    inactive_users = User.query.filter(User.latest_loggedin < twenty_four_hours_ago).filter(User.is_librarian == False).all()
    message = f"""
    

    We haven't seen you at the library in 24 hours! Just a friendly reminder that there are many new books waiting to be discovered. Come visit us soon and explore our latest collection!

    Happy reading,
    The Library Team
    """
    print("list of  inactive users",inactive_users)
    for user in inactive_users:
        subject = "Haven't seen you at the library lately!"
        to = user.email
        html = render_template('daily.html', user=user, message=message)
        send_email(to,subject,  html)
        print("Reminder email Sent to ", user.name)

        
    return "SUCCESS"


@celery.task
def monthly_report():
    users = User.query.filter_by(is_librarian=False).all()


    for user  in users:
        one_month_ago = datetime.now() - timedelta(days=30)
        user_issues = Issues.query.filter_by(user_id=user.id).filter(Issues.date > one_month_ago).all()


        issue_details = []
        total_book_issued = 0

        for issue in user_issues:
            total_book_issued+=1

            issue_details.append({
                'issue_date': issue.date.strftime('%Y-%m-%d %H:%M'),
                'total_book_issued': total_book_issued,
                'Book_Name': issue.bookIssue.name
            })
        html = render_template('monthly_report.html', user=user, issue_details=issue_details, total_book_issued=total_book_issued)
        send_email(subject = "Monthly Report", to = user.email, html = html)

    return "success"

#########################################################################################

mail = Mail()
@celery.task
def export_csv(librarian_id, email):
    books_issued = Issues.query.all()
    filename = f'admin_report.csv'
    filepath = os.path.join('exports', filename)
    
    os.makedirs('exports', exist_ok=True)
    
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Issue_Id', 'Book_Name', 'Content', 'Authors', 'Date_Issued', 'Return_Date', 'User_Id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for issue in books_issued:
            writer.writerow({
                'Issue_Id': issue.id,
                'User_Id': issue.user_id,
                'Book_Name': issue.bookIssue.name,
                'Content': issue.bookIssue.content,
                'Authors': issue.bookIssue.author_name,
                'Date_Issued': issue.date
            })
    
    Send_email(email, filename)


def Send_email(to, filename):
    csv_report_download_url = f'http://localhost:5000/download/{filename}'
    
    html = f"""
    <p>Just a quick note to let you know that your e-book export is all set and ready to go!
            🎉 You can grab your report by clicking the download button below:</p>
    <p><a href="{csv_report_download_url}">Download</a></p>
    """
    
    msg = Message("Export CSV Report", recipients=[to],sender='noreply@library.com')
    msg.body = "The export for the csv admin report has been completed. You can download the file from the link below:\n\n" + csv_report_download_url
    msg.html = html
    
    mail.send(msg)