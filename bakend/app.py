from flask import Flask,request,jsonify,send_file,send_from_directory
from config import Config
from models import *
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, unset_jwt_cookies
import os
import io
import matplotlib.pyplot as plt
import workers,task
from flask_mail import Mail
from flask_caching import Cache



app=Flask(__name__)
app.config.from_object(Config)

celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND']
)

celery.Task = workers.ContextTask
app.app_context().push()

jwt=JWTManager(app)
mail = Mail(app)
db.init_app(app)
cache = Cache(app)
ma.init_app(app)
bcrypt.init_app(app)                                                              

with app.app_context():
    db.create_all()

    # it will create librarian by default
    librarian=User.query.filter_by (is_librarian=True).first()
    if not librarian:
        librarian=User(email='admin@gmail.com',password='0',name='Librarian',is_librarian=True , latest_loggedin=datetime.now())
        db.session.add(librarian)
        db.session.commit()


CORS(app, supports_credentials=True)

@app.route('/',methods=['GET'])
def home():
    print("ewfiefifohf")
    # task.daily_reminder.delay()
    # task.multiply.delay(3,4)
    # task.add.delay()
    return "Hello World"

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   #REGISTER API

@app.route('/userregister', methods=['POST'])            
def userRegister():
    data = request.json
    email = data["email"]
    password = data["password"]
    name = data["name"]
    latest_loggedin = datetime.now()

    if not email or not name or not password:
        return {"error": "All fields are required"}, 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "User already exists"}, 409

    new_user = User(email=email, password=password, name=name, latest_loggedin=latest_loggedin)

    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to create user: {str(e)}"}, 500



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    #LOGIN API

@app.route("/userlogin", methods= ["POST"])                   
def userLogin():
    data = request.json
    name = data["name"]
    email = data["email"]
    password = data["password"]

    if not name or not email or not password:
        return {"error": "Name and Email and password are required"}, 400
    
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"error": "Invalid Credentials"}, 401
    
    access_token = create_access_token(identity={
        "id":user.id,
        "email": user.email,
        "name": user.name,
        "is_librarian":user.is_librarian
    })

    user.latest_loggedin = datetime.now()
    db.session.commit()

    return jsonify({"access_token": access_token, "message": "Login successful","is_librarian":user.is_librarian}), 200   
   


# THIS ROUTE TO BE ACCESSIBLE ONLY BY LOGGED IN USERS
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print(current_user["role"])
    return jsonify(logged_in_as=current_user), 200


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   #LOGOUT API

@app.route('/logout', methods=['POST'])                                     
@jwt_required()
def logout():
    response = jsonify({'message': 'logout successful'})
    unset_jwt_cookies(response)
    return response

@app.route("/getuserinfo", methods= ["GET"])
@jwt_required()
def get_userinfo():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user["email"]).first()
    user_data={'id':user.id,'name':user.name,'is_librarian':user.is_librarian,'email':user.email}
    return jsonify(user_data), 200



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  crud on section

# Creating a Section
@app.route("/section/add", methods= ["POST"])                         #CREATING SECTION
@jwt_required()
def createSection():
    this_user = get_jwt_identity()
    # Only for admin
    if not this_user["is_librarian"] :
        return {"error": "Unauthorized"}, 401
    
    data = request.json
    name = data["name"]
    if not name:
        return {"error": "Name is required"}, 400
    

    existing_section = Section.query.filter_by(name=name).first()
    if existing_section:
        return {"error": "Section already exists"}, 409
    new_section = Section(name=name)
    try: 
        db.session.add(new_section)
        db.session.commit()
        return {"message": "Section created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to create category: {str(e)}"}, 500


@app.route("/sections", methods= ["GET"])                             #ALL SECTION API
def get_sections():
    sections = Section.query.all()
    sections_data = []
    for section in sections:
        book_count = Book.query.filter_by(section_id=section.id).count()
        sections_data.append({
            'id': section.id,
            'name': section.name,
            'book_count': book_count
        })
    return jsonify(sections_data)

@app.route("/section/<int:id>", methods= ["GET"])                       #FETCHING SECTION BY ID
def get_section(id):
    section = Section.query.filter_by(id=id).first() 
    if not section:
        return {"error": "Section not found"}, 404
    section_data = section_schema.dump(section)
    return jsonify(section_data), 200

@app.route("/section/update/<int:id>", methods= ["PUT"])               #UPDATING SECTION
@jwt_required()
def updateSection(id):
    this_user = get_jwt_identity()

    if not this_user["is_librarian"] :
        return {"error": "Unauthorized"}, 401
    
    data = request.json
    name = data["name"]
    if not name:
        return {"error": "Name is required"}, 400
    section = Section.query.get(id)
    if not section:
        return {"error": "Section not found"}, 404
    existing_section = Section.query.filter_by(name=name).first()

    if existing_section and existing_section.id != id:
        return {"error": "Section already exists"}, 409
    
    section.name = name
    try: 
        db.session.commit()
        return {"message": "Section updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update section: {str(e)}"}, 500

@app.route("/section/delete/<int:id>", methods= ["DELETE"])                     #DELETING SECTION
@jwt_required()
def delete_section(id):
    this_user = get_jwt_identity()

    if not this_user["is_librarian"] :
        return {"error": "Unauthorized"}, 401
    
    section = Section.query.get(id)
    if not section:
        return {"error": "Section not found"}, 404
    
    try:
        db.session.delete(section)
        db.session.commit()
        return {"message": "Section deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete section: {str(e)}"}, 500



#########################################################  crud on book

@app.route("/section/<int:id>/book/add", methods= ["POST"])                         #ADDING BOOK
@jwt_required()
def addBook(id):
    this_user = get_jwt_identity()

    if not this_user["is_librarian"] :
        return {"error": "Unauthorized"}, 401
    
    data = request.json
    name = data["name"]
    author_name = data["author_name"]
    content = data["content"]

    if not name or not author_name or not content:
        return {"error": "All fields are required"}, 400
    
    section = Section.query.get(id)
    if not section:
        return {"error": "Section not found"}, 404

    new_book = Book(
        name=name, 
        section_id=section.id,
        author_name = author_name,
        content= content)
    
    try: 
        db.session.add(new_book)
        db.session.commit()
        return {"message": "Book added successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to add book: {str(e)}"}, 500


@app.route("/books", methods= ["GET"])                           #ALL BOOKS API
def get_all_books():
    books = Book.query.all()
    books_data = books_schema.dump(books)
    return jsonify(books_data), 200


@app.route("/book/<int:id>", methods= ["GET"])                     #GETTING BOOK BY ID
def get_book(id):
    book = Book.query.filter_by(id=id).first() 
    if not book:
        return {"error": "Book not found"}, 404
    book_data = book_schema.dump(book)
    return jsonify(book_data), 200


@app.route("/book/update/<int:id>", methods= ["PUT"])                    #UPDATE BOOK API
@jwt_required()
def update_book(id):
    this_user = get_jwt_identity()

    if not this_user["is_librarian"] :
        return {"error": "Unauthorized"}, 401
    
    data = request.json
    name = data["name"]
    author_name = data["author_name"]
    content = data["content"]
    section_id = data["section_id"]

    if not name or not author_name or not content or not section_id:
        return {"error": "All fields are required"}, 400
    
    book = Book.query.get(id)
    if not book:
        return {"error": "Book not found"}, 404
    
    book.name = name
    book.author_nam = author_name
    book.content = content
    book.section_id = section_id
    try: 
        db.session.commit()
        return {"message": "Book updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update book: {str(e)}"}, 500


@app.route("/book/<int:id>", methods= ["DELETE"])                      #DELETING BOOK
@jwt_required()
def delete_book(id):
    this_user = get_jwt_identity()

    if not this_user["is_librarian"] :
        return {"error": "Unauthorized"}, 401
    
    book = Book.query.get(id)
    if not book:
        return {"error": "Book not found"}, 404
    
    try:
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete book: {str(e)}"}, 500
    
@app.route("/getallbookinfo", methods=["GET"])          ### getting book details 
# @cache.cached(timeout=60)
def getallbookinfo():
    sections = Section.query.all()
    data = []

    for section in sections:
        data.append({
            "id": section.id,
            "name": section.name,
            "books": books_schema.dump(section.books)
        })
    return jsonify(data), 200

@app.route("/section/<int:id>/book" , methods=["GET"])            ###view book
def viewBook(id):
    section=Section.query.filter_by(id=id).first()
    books=books_schema.dump(section.books)
    return jsonify(books), 200

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4    admin functionality

@app.route('/bookrequested')                ###########  showing books requested 
def bookRequested():
    requests = Request.query.all()
    requests_data = [{'id': request.id, 'user_id': request.user_id, 'book_id': request.book_id} for request in requests]
    return jsonify(requests_data)



@app.route('/reject/<int:id>',methods=["DELETE"])                                   #rejecting a book request
def rejectRequest(id):
    request=Request.query.get(id)
    if not request:
          return jsonify({"error": "Request not found"}), 404
    
    
    try:
        db.session.delete(request)
        db.session.commit()
        return {"message": "Request rejected successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete request: {str(e)}"}, 500
    

@app.route('/accept/<int:id>',methods=["POST"])                              #accepting a book request
def acceptRequest(id):
    current_date = datetime.now()
    request=Request.query.get(id)
    issue=Issues(user_id=request.user_id,book_id=request.book_id,date=current_date)
    
    try:
        db.session.delete(request)
        db.session.commit()
        db.session.add(issue)
        db.session.commit()
        return {"message": "Request accepted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to accept request: {str(e)}"}, 500
    
   
@app.route('/revoke/<int:id>',methods=["DELETE"])                         #revoking issued book
def revokeBook(id):
    issue=Issues.query.get(id)
    
    try:
        db.session.delete(issue)
        db.session.commit()
        return {"message": "Book Revoked Successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to revoke Book: {str(e)}"}, 500
    

@app.route('/bookstatus')                         ############  book status of issued book
def book_status():
    books = Book.query.all()
    issues = Issues.query.all()

    if not books:
        return jsonify({'error': 'No books found'}), 404

    if not issues:
        return jsonify({'error': 'No issues found'}), 404

    
    books_data = [{'id': book.id, 'name': book.name, 'author_name': book.author_name} for book in books]
    issues_data = [{'id': issue.id, 'book_id': issue.book_id, 'user_id': issue.user_id} for issue in issues]

    return jsonify({'books': books_data, 'issues': issues_data})




@app.route('/book-issued-history-report', methods=['GET'])           #####  showing bar graph to admin
def book_issued_history_report():
    
    books = Book.query.all()
    sections = Section.query.all()
    issues = Issues.query.all()
    requests = Request.query.all()
    
    categories = ['Sections', 'Books', 'Books Requested', 'Books Issued']
    counts = [len(sections), len(books), len(requests), len(issues)]
    
    plt.clf()
    plt.bar(categories, counts, color='skyblue')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    
    response = {
        'sections': counts[0],
        'books': counts[1],
        'requests': counts[2],
        'issued': counts[3]
    }
    print(response)
    return jsonify(response)
   
@app.route('/stats', methods=['GET'])         #### used for fetching graph
# @jwt_required()
def stats():
    # this_user = get_jwt_identity()

    # if not this_user["is_librarian"] :
    #     return {"error": "Unauthorized"}, 401
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')


 
@app.route('/issue-section-pie-chart', methods=['GET'])         ######   bar graoh display
# @jwt_required()
def issued_book_section_pie_chart():
    # this_user = get_jwt_identity()

    # if not this_user["is_librarian"] :
    #     return {"error": "Unauthorized"}, 401
    
    issues = Issues.query.all()

    section_counts = {}
    for issue in issues:
        section_name = issue.bookIssue.section.name
        print(section_name)
        if section_name not in section_counts:
            section_counts[section_name] = 0
        section_counts[section_name] += 1

    plt.figure(figsize=(10, 6))
    plt.pie(section_counts.values(), labels=section_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')



from task import export_csv

@app.route('/export_csv_report', methods=['GET'])          #export csv report route
def export_csv_report():
    librarian_id = request.args.get('librarian_id', 1)
    email = request.args.get('email', 'admin@gmail.com')
    task = export_csv.apply_async(args=[librarian_id, email])
    return jsonify({"task_id": task.id, "status": "Export task started"}), 202

@app.route('/download/<filename>')            #download csv report 
def download_file(filename):
    return send_from_directory('exports', filename)
        


       


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ user functionality

@app.route('/request/<int:id>',methods= ["POST"])              #requesting book
@jwt_required()
def requestBook(id):                                               
    this_user = get_jwt_identity()

    if  this_user["is_librarian"] :
        return {"error": "Only user can excess this page"}, 401
    
    userID =this_user["id"]
    
    book=Book.query.filter_by(id=id).first()
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    
    prev_request=Request.query.filter_by(user_id=userID).count()
    if prev_request>4:
        return jsonify({"error": "Max Request Exceeded"}), 429
    
    newRequest = Request(user_id=  userID, book_id=id)

    try:
        db.session.add(newRequest)
        db.session.commit()
        return jsonify({"message": "Book request submitted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to request book: {str(e)}"}, 500
    


    

@app.route('/issued')                                    #showing issued book
@jwt_required()
def issuedbook():
    this_user = get_jwt_identity()
    user = User.query.get(this_user["id"])
    if not user:
        return jsonify({"msg": "User not found"}), 404
    issues=Issues.query.filter_by(user_id=user.id).all()
    
    issued_books = []
    for issue in issues:
        book = Book.query.get(issue.book_id)
        issued_books.append({
            "book_id": book.id,
            "issue_id":issue.id,
            "name": book.name,
            "author_name": book.author_name,
            "content":book.content,
        })
        print(issued_books)

    return jsonify({
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "issued_books": issued_books
    })




@app.route('/return/<int:id>', methods=['DELETE'])             ###########  returning issued book by user
def returnBook(id):
    issue = Issues.query.get(id)
    if not issue:
        return jsonify({"error": "Issue id not found"}), 404
    
    
    try:
        db.session.delete(issue)
        db.session.commit()
        return {"message": "Book Returned Successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to return Book: {str(e)}"}, 500
    








@app.route('/submitFeedback', methods=['POST'])    #####  feedback to issued book
def submit_feedback():
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    content = data.get('content')
    
    if not user_id or not book_id or not content:
        return jsonify({'error': 'Please fill out all details'}), 400
    
    feedback = Feedback(user_id=user_id, book_id=book_id, content=content)
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({'message': 'Feedback submitted successfully'}), 201








# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# from flask import Response
# from io import StringIO
# import csv
# def generate_issue_csv():
#     issues = Issues.query.all()
#     csv_buffer = StringIO()
#     csv_writer = csv.writer(csv_buffer)
#     csv_writer.writerow(['Issue_Id','User_Id', 'Book_Name', 'Content', 'Authors', 'Date_Issued'])
#     for issue in issues:
#         csv_writer.writerow([issue.id, issue.user_id, issue.bookIssue.name, issue.bookIssue.content, issue.bookIssue.author_name, issue.date])

#     return csv_buffer.getvalue()

# @app.route('/download-issue-csv', methods=['GET'])
# # @cache.cached(timeout=600)
# def download_issue_csv():
#     csv_data = generate_issue_csv()
#     return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=Issued_book_report.csv'})



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if __name__=="__main__":
    app.run(debug=True)






