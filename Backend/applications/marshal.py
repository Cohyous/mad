from flask_restful import fields

def format_date(date):
    return date.strftime("%Y-%m-%d") if date else None

book = {
    "id": fields.Integer,
    "isbn_no": fields.Integer,
    "author": fields.String,
    "price": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "date_published": fields.String(attribute=lambda x: format_date(x.date_published)),
    "section_id": fields.Integer,
    "avg_rating": fields.Float,
    "total_ratings": fields.Integer
}
category = {
    "SectionID": fields.Integer,
    "Genre": fields.String
}
feedback = {
    "id": fields.Integer,
    "feedback": fields.String,
    "stars": fields.Integer
}
