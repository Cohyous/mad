from sqlite3 import IntegrityError
from flask_restful import Resource, marshal_with
from flask import make_response, jsonify, request as req
from flask_security import auth_token_required, roles_required, roles_accepted, current_user,auth_required
from applications.model import *
# from applications.model import Product as prd
from applications.marshal import *
from datetime import date, datetime, timedelta

from flask_restful import Resource, marshal_with, reqparse
from flask import make_response, jsonify, request as req
from applications.model import *
from applications.marshal import *
from datetime import datetime
from sqlalchemy import and_, desc, func


class MostRatedBooks(Resource):
    @marshal_with(book)
    
    def get(self):
        books = db.session.query(Books, func.coalesce(func.avg(Feedbacks.stars), 0).label('avg_rating')) \
            .outerjoin(Feedbacks, Books.id == Feedbacks.book_id) \
            .group_by(Books.id) \
            .order_by(desc('avg_rating')) \
            .limit(10) \
            .all()
        books = [book for book, avg_rating in books]
        return books


class BestSellers(Resource):
    @marshal_with(book)
    def get(self):
        best_sellers = Transaction.query \
            .with_entities(Transaction.book_id, db.func.count(Transaction.book_id).label('total')) \
            .group_by(Transaction.book_id) \
            .order_by(desc('total')) \
            .limit(10).all()

        book_ids = [b.book_id for b in best_sellers]
        books = Books.query.filter(Books.id.in_(book_ids)).all()
        return books


class NewlyAddedBooks(Resource):
    @marshal_with(book)
    def get(self):
        books = Books.query.order_by(
            desc(Books.date_published)).limit(10).all()
        return books


class OwnedBooksAPI(Resource):
    @auth_token_required
    @roles_accepted('user')
    @marshal_with(book)
    def get(self):
        owned_books = OwnedBooks.query.filter_by(user_id=current_user.id).all()
        book_ids = [ob.book_id for ob in owned_books]
        books = Books.query.filter(Books.id.in_(book_ids)).all()
        return books


class BorrowedBooksAPI(Resource):
    @auth_token_required
    @roles_accepted('user')
    @marshal_with(book)
    def get(self):
        today = date.today()

        # Delete expired borrowed books
        BorrowedBooks.query.filter(and_(
            BorrowedBooks.user_id == current_user.id, BorrowedBooks.date_to < today)).delete()
        db.session.commit()

        # Fetch current borrowed books
        borrowed_books = BorrowedBooks.query.filter(and_(
            BorrowedBooks.user_id == current_user.id, BorrowedBooks.date_to >= today)).all()
        book_ids = [bb.book_id for bb in borrowed_books]
        books = Books.query.filter(Books.id.in_(book_ids)).all()
        return books
  # Assuming the models are imported from a models module


class SearchBooksAPI(Resource):
    @marshal_with(book)
    def get(self):
        # Obtain query parameters

        filter = req.args.get('filter')
        value = req.args.get('value')

        if filter == "name":
            books = Books.query.filter(Books.name.like(f'%{value}%')).all()
        elif filter == "author":
            books = Books.query.filter(Books.author.like(f'%{value}%')).all()
        elif filter == "id":
            books = Books.query.filter(Books.id == int(value)).all()
        else:
            return make_response(jsonify({'message': 'Invalid filter type'}), 400)

        return books


class BookFeedbacks(Resource):
    @auth_required
    @roles_accepted('user')
    def get(self, book_id):
        book = Books.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        feedbacks = Feedbacks.query.filter_by(book_id=book_id).all()
        avg_stars = db.session.query(
            func.avg(Feedbacks.stars)).filter_by(book_id=book_id).scalar()
        avg_stars = avg_stars if avg_stars else 0

        feedbacks_response = []
        for feedback in feedbacks:
            feedbacks_response.append({
                'id': feedback.id,
                'feedback': feedback.feedback,
                'stars': feedback.stars
            })

        response = {
            'book_id': book_id,
            'average_rating': avg_stars,
            'feedbacks': feedbacks_response
        }

        return make_response(jsonify(response), 200)

    @auth_token_required
    @roles_accepted('user')
    def post(self, book_id):
        args = feedback_parser.parse_args()
        stars = args['stars']
        feedback_text = args['feedback']

        book = Books.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        existing_feedback = Feedbacks.query.filter_by(
            user_id=current_user.id, book_id=book_id).first()

        if existing_feedback:
            existing_feedback.stars = stars
            existing_feedback.feedback = feedback_text
        else:
            new_feedback = Feedbacks(
                user_id=current_user.id,
                book_id=book_id,
                stars=stars,
                feedback=feedback_text
            )
            db.session.add(new_feedback)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'message': 'Error saving feedback'}), 500)

        return make_response(jsonify({'message': 'Feedback submitted successfully'}), 200)


request_parser = reqparse.RequestParser()
request_parser.add_argument(
    'book_id', type=int, required=True, help='Book ID is required')


class UserEligibilityAPI(Resource):
    @auth_token_required
    def post(self):
        return "This works"
    @auth_token_required
    @roles_accepted('user','librarian')
    def get(self):
        user_id = current_user.id
        if current_user.has_role('user'):
            user_id = current_user.id
            print(user_id)
            # Fetch user's owned books
            owned_books = OwnedBooks.query.filter_by(user_id=user_id).all()
            owned_book_ids = {book.book_id for book in owned_books}

            # Fetch user's requests
            requests = Requests.query.filter_by(user_id=user_id).all()
            requested_book_ids = {req.book_id for req in requests}

            # Fetch user's borrowed books that are not expired
            borrowed_books = BorrowedBooks.query.filter(
                BorrowedBooks.user_id == user_id, BorrowedBooks.date_to >= date.today()).all()
            borrowed_book_ids = {borrow.book_id for borrow in borrowed_books}

            return make_response(jsonify({'owned_books': list(owned_book_ids), 'requested_books': list(requested_book_ids), 'borrowed_books': list(borrowed_book_ids)}),200)
        
        elif current_user.has_role('librarian'):
            print(user_id)
            return make_response(jsonify({'message':'You are a librarian'}),200)


class UserRequestAPI(Resource):
    @auth_token_required
    @roles_accepted('user')
    def post(self):
        args = request_parser.parse_args()
        book_id = args['book_id']
        user_id = current_user.id

        # Check if the book is already owned by the user
        if OwnedBooks.query.filter_by(user_id=user_id, book_id=book_id).first():
            return make_response(jsonify({'message': 'You already own this book'}), 400)

        # Check if the book is already requested by the user
        if Requests.query.filter_by(user_id=user_id, book_id=book_id).first():
            return make_response(jsonify({'message': 'You have already requested this book'}), 400)

        # Check if the book is already borrowed and not yet returned
        if BorrowedBooks.query.filter(BorrowedBooks.user_id == user_id, BorrowedBooks.book_id == book_id, BorrowedBooks.date_to >= date.today()).first():
            return make_response(jsonify({'message': 'You have already borrowed this book'}), 400)

        # Check the number of requests and borrowed books
        request_count = Requests.query.filter_by(user_id=user_id).count()
        borrowed_count = BorrowedBooks.query.filter(
            BorrowedBooks.user_id == user_id, BorrowedBooks.date_to >= date.today()).count()

        if request_count >= 5:
            return make_response(jsonify({'message': 'You cannot request more than 5 books'}), 400)

        if borrowed_count >= 5:
            return make_response(jsonify({'message': 'You cannot borrow more than 5 books'}), 400)

        # If all checks pass, add the request to the Requests table
        new_request = Requests(
            user_id=user_id,
            book_id=book_id,
            requested_days=14,  # Default request days
            date_of_issue=date.today()
        )
        db.session.add(new_request)
        db.session.commit()

        return make_response(jsonify({'message': 'Book requested successfully'}), 200)


class UserPurchaseAPI(Resource):
    @auth_token_required
    @roles_accepted('user')
    def post(self):
        args = request_parser.parse_args()
        book_id = args['book_id']
        user_id = current_user.id

        # Check if the book is already owned
        if OwnedBooks.query.filter_by(user_id=user_id, book_id=book_id).first():
            return make_response(jsonify({'message': 'You already own this book'}), 400)

        # Add the book to the OwnedBooks table
        new_owned_book = OwnedBooks(
            user_id=user_id,
            book_id=book_id,
            date_of_purchase=date.today()
        )
        db.session.add(new_owned_book)
        db.session.commit()

        return make_response(jsonify({'message': 'Book purchased successfully'}), 200)


class LibrarianUserRequestsAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def get(self, user_id):
        requests = Requests.query.filter_by(user_id=user_id).all()

        if not requests:
            return make_response(jsonify({'message': 'No requests found for this user'}), 404)

        requests_response = []
        for req in requests:
            requests_response.append({
                'id': req.id,
                'book_id': req.book_id,
                'user_id': req.user_id,
                'requested_days': req.requested_days,
                'date_of_issue': req.date_of_issue
            })

        response = {
            'user_id': user_id,
            'requests': requests_response
        }

        return make_response(jsonify(response), 200)


class LibrarianManageRequestAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def post(self, request_id, action):
        request_entry = Requests.query.get(request_id)

        if not request_entry:
            return make_response(jsonify({'message': 'Request not found'}), 404)

        if action not in ['accept', 'reject']:
            return make_response(jsonify({'message': 'Invalid action'}), 400)

        if action == 'accept':
            # Remove from Requests table
            db.session.delete(request_entry)
            db.session.commit()

            # Add to BorrowedBooks table
            new_borrowed_book = BorrowedBooks(
                user_id=request_entry.user_id,
                book_id=request_entry.book_id,
                date_from=date.today(),
                date_to=date.today() + timedelta(days=request_entry.requested_days),
                approved_admin_id=current_user.id  # Assuming the current librarian is approving
            )
            db.session.add(new_borrowed_book)
        elif action == 'reject':
            # Just remove from Requests table
            db.session.delete(request_entry)

        db.session.commit()

        return make_response(jsonify({'message': f'Request {action}ed successfully'}), 200)


# Add the endpoint to the API
class LibrarianEditDeleteBookAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('author', type=str)
        parser.add_argument('isbn_no', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('date_published', type=str)
        parser.add_argument('section_id', type=int)
        args = parser.parse_args()

        book = Books.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        if args['name']:
            book.name = args['name']
        if args['author']:
            book.author = args['author']
        if args['isbn_no']:
            book.isbn_no = args['isbn_no']
        if args['price']:
            book.price = args['price']
        if args['date_published']:
            try:
                book.date_published = datetime.strptime(
                    args['date_published'], '%Y-%m-%d').date()
            except ValueError:
                return make_response(jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400)
        if args['section_id']:
            book.section_id = args['section_id']

        db.session.commit()
        return make_response(jsonify({'message': 'Book information updated successfully'}), 200)

    @auth_token_required
    @roles_accepted('librarian')
    def delete(self, book_id):
        book = Books.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        db.session.delete(book)
        db.session.commit()
        return make_response(jsonify({'message': 'Book deleted successfully'}), 200)


class LibrarianEditSectionAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def put(self, section_id):
        parser = reqparse.RequestParser()
        parser.add_argument('genre', type=str, required=True,
                            help='Genre cannot be blank')
        args = parser.parse_args()

        section = Section.query.get(section_id)
        if not section:
            return make_response(jsonify({'message': 'Section not found'}), 404)

        section.genre = args['genre']
        db.session.commit()
        return make_response(jsonify({'message': 'Section genre updated successfully'}), 200)


class LibrarianEditDeleteBookAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('author', type=str)
        parser.add_argument('isbn_no', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('date_published', type=str)
        parser.add_argument('section_id', type=int)
        args = parser.parse_args()

        book = Books.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        if args['name']:
            book.name = args['name']
        if args['author']:
            book.author = args['author']
        if args['isbn_no']:
            book.isbn_no = args['isbn_no']
        if args['price']:
            book.price = args['price']
        if args['date_published']:
            try:
                book.date_published = datetime.strptime(
                    args['date_published'], '%Y-%m-%d').date()
            except ValueError:
                return make_response(jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400)
        if args['section_id']:
            book.section_id = args['section_id']

        db.session.commit()
        return make_response(jsonify({'message': 'Book information updated successfully'}), 200)

    @auth_token_required
    @roles_accepted('librarian')
    def delete(self, book_id):
        book = Books.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        db.session.delete(book)
        db.session.commit()
        return make_response(jsonify({'message': 'Book deleted successfully'}), 200)


class LibrarianEditSectionAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def put(self, section_id):
        parser = reqparse.RequestParser()
        parser.add_argument('genre', type=str, required=True,
                            help='Genre cannot be blank')
        args = parser.parse_args()

        section = Section.query.get(section_id)
        if not section:
            return make_response(jsonify({'message': 'Section not found'}), 404)

        section.genre = args['genre']
        db.session.commit()
        return make_response(jsonify({'message': 'Section genre updated successfully'}), 200)


class UserInfoAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        # Fetch owned books
        owned_books = db.session.query(Books).join(
            OwnedBooks).filter(OwnedBooks.user_id == user_id).all()

        # Fetch borrowed books
        borrowed_books = db.session.query(Books, BorrowedBooks.date_from, BorrowedBooks.date_to, Admin.admin_name) \
            .join(BorrowedBooks, Books.id == BorrowedBooks.book_id) \
            .outerjoin(Admin, BorrowedBooks.approved_admin_id == Admin.id) \
            .filter(BorrowedBooks.user_id == user_id).all()

        borrowed_books_info = [{
            'book_id': book.id,
            'name': book.name,
            'author': book.author,
            'date_from': date_from,
            'date_to': date_to,
            'approved_admin': admin_name
        } for book, date_from, date_to, admin_name in borrowed_books]

        response = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'owned_books': [{'id': book.id, 'name': book.name} for book in owned_books],
            'borrowed_books': borrowed_books_info
        }

        return make_response(jsonify(response), 200)


remove_borrowed_parser = reqparse.RequestParser()
remove_borrowed_parser.add_argument(
    'book_id', type=int, required=True, help='Book ID is required')


class RemoveBorrowedBookAPI(Resource):
    @auth_token_required
    @roles_accepted('librarian')
    def post(self):
        args = remove_borrowed_parser.parse_args()
        book_id = args['book_id']

        # Find the borrowed book entry
        borrowed_entry = BorrowedBooks.query.filter_by(book_id=book_id).first()

        if not borrowed_entry:
            return make_response(jsonify({'message': 'Borrowed book entry not found'}), 404)

        # Remove the borrowed book entry
        db.session.delete(borrowed_entry)
        db.session.commit()

        return make_response(jsonify({'message': 'Borrowed book entry removed successfully'}), 200)
