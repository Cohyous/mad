from flask import Flask
from applications.database import db
from applications.model import User, Role
from applications.config import Config
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security, hash_password
from applications.user_datastore import user_datastore
from seed_data import seed_books

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)



    api = Api(app, prefix='/api/v1')
    
    app.security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()
        seed_books()
        librarian = app.security.datastore.find_or_create_role(name='librarian', description='Administrator')
        user = app.security.datastore.find_or_create_role(name='user', description='Customer')
        if not app.security.datastore.find_user(email="admin@gmail.com"):
            app.security.datastore.create_user(email="admin@gmail.com", username='admin', password=hash_password("password"), roles=[librarian])
        db.session.commit()
        
    return app, api

app, api = create_app()

from applications.auth_api import *
api.add_resource(Login,"/login")
api.add_resource(Register,'/register')
api.add_resource(Logout,'/logout')


from applications.library_management_api import *

api.add_resource(MostRatedBooks, '/most_rated_books')
api.add_resource(BestSellers, '/best_sellers')
api.add_resource(NewlyAddedBooks, '/newly_added_books')
api.add_resource(OwnedBooksAPI, '/owned_books')
api.add_resource(BorrowedBooksAPI, '/borrowed_books')
api.add_resource(SearchBooksAPI, '/search_books')
api.add_resource(BookFeedbacks, '/book_feedbacks/<int:book_id>')
api.add_resource(UserEligibilityAPI, '/user_eligibility')
api.add_resource(UserRequestAPI, '/user_request')
api.add_resource(UserPurchaseAPI, '/user_purchase')
api.add_resource(LibrarianUserRequestsAPI, '/librarian/user_requests/<int:user_id>')
api.add_resource(LibrarianManageRequestAPI, '/librarian/manage_request/<int:request_id>/<string:action>')
api.add_resource(LibrarianEditDeleteBookAPI, '/librarian/edit_delete_book/<int:book_id>')
api.add_resource(LibrarianEditSectionAPI, '/librarian/edit_section/<int:section_id>')
api.add_resource(UserInfoAPI, '/user_info/<int:user_id>')
api.add_resource(RemoveBorrowedBookAPI, '/librarian/remove_borrowed_book')

@app.route('/')
def index():
    return ({"message": "Welcome to the Flask application!"})

if __name__ == '__main__':
    app.run(debug=True)

