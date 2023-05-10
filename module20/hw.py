from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Date, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
app = Flask(__name__)
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def __repr__(self):
        return f'<Student {self.name} {self.surname}>'

    @classmethod
    def get_students_in_dorm(cls):
        return cls.query.filter_by(dormitory=True).all()

    @classmethod
    def get_students_with_average_score_above(cls, score):
        return cls.query.filter(cls.average_score > score).all()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return is None:
            return (datetime.now() - self.date_of_issue).days
        else:
            return (self.date_of_return - self.date_of_issue).days


@app.route('/books', methods=['GET'])
def get_books():
    books = session.query(Book).all()
    return jsonify([book.serialize() for book in books])


@app.route('/overdue', methods=['GET'])
def overdue_students():
    due_date = datetime.now() - timedelta(days=14)
    borrowed_books = session.query(ReceivingBook).filter(ReceivingBook.date_of_return == None).all()

    overdue_students = []

    for book in borrowed_books:
        if book.date_of_issue < due_date:

            student = session.query(Student).filter(Student.id == book.student_id).one()
            overdue_students.append({'name': student.name, 'surname': student.surname})

    return jsonify({'overdue_students': overdue_students})


@app.route('/issue_book', methods=['POST'])
def issue_book():
    book_id = request.json.get('book_id')
    student_id = request.json.get('student_id')
    date_of_issue = datetime.now()
    date_of_return = date_of_issue + timedelta(days=14)

    book = Book.query.filter_by(id=book_id).first()
    student = Student.query.filter_by(id=student_id).first()

    if book is None or student is None:
        return jsonify({'error': 'Book or student not found'}), 404

    if book.count == 0:
        return jsonify({'error': 'No books available'}), 400

    receiving_book = ReceivingBook(book_id=book_id, student_id=student_id,
                                   date_of_issue=date_of_issue,
                                   date_of_return=date_of_return)
    session.add(receiving_book)
    session.commit()

    book.count -= 1
    session.commit()

    return jsonify({'message': 'Book issued successfully'}), 200


@app.route('/return-book', methods=['POST'])
def return_book():
    book_id = request.json['book_id']
    student_id = request.json['student_id']

    receiving_book = session.query(ReceivingBook).filter_by(
        book_id=book_id,
        student_id=student_id,
        date_of_return=None).first()

    if not receiving_book:
        return jsonify({'error': 'Такой связки книги и студента не найдено'}), 404

    receiving_book.date_of_return = datetime.now()

    book = session.query(Book).filter_by(id=book_id).first()
    book.count += 1
    session.commit()

    return jsonify({'message': 'Книга успешно возвращена в библиотеку'}), 200


@app.route('/books/search')
def search_books():
    search_string = request.args.get('query')

    books = session.query(Book).filter(Book.name.ilike(f"%{search_string}%")).all()

    book_list = []
    for book in books:
        book_list.append({
            'id': book.id,
            'name': book.name,
            'count': book.count,
            'release_date': book.release_date,
            'author_id': book.author_id
        })

    return jsonify(book_list)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
