import csv
from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Date, \
    create_engine, ForeignKey, Table, extract, func, desc
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, relationship, joinedload, backref

Base = declarative_base()
app = Flask(__name__)
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()

students_receiving_books = Table('students_receiving_books', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('receiving_book_id', Integer, ForeignKey('receiving_books.id'), primary_key=True)
)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship('Author', backref='books', cascade='save-update')
    students_association = association_proxy('students', 'student')


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
    receiving_books_association = association_proxy('receiving_books', 'book')
    receiving_books = relationship('ReceivingBook', secondary=students_receiving_books, backref='students_books')


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
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    book = relationship('Book', backref=backref('receiving_books', cascade='all, delete-orphan'))
    student = relationship('Student', backref=backref('receiving_books_associated', cascade='all, delete-orphan'))

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return is None:
            return (datetime.now() - self.date_of_issue).days
        else:
            return (self.date_of_return - self.date_of_issue).days


@app.route('/books', methods=['GET'])
def get_books():
    books = session.query(Book).options(joinedload()).all()

    return jsonify([book.serialize() for book in books])


@app.route('/overdue', methods=['GET'])
def overdue_students():
    due_date = datetime.now() - timedelta(days=14)
    borrowed_books = session.query(ReceivingBook).filter(
        ReceivingBook.date_of_return == None).all()

    overdue_students = []

    for book in borrowed_books:
        if book.date_of_issue < due_date:
            student = session.query(Student).filter(
                Student.id == book.student_id).one()
            overdue_students.append(
                {'name': student.name, 'surname': student.surname})

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
        return jsonify(
            {'error': 'Такой связки книги и студента не найдено'}), 404

    receiving_book.date_of_return = datetime.now()
    book = session.query(Book).options(
        joinedload('receiving_books')).filter_by(id=book_id).first()

    book.count += 1
    session.commit()

    return jsonify({'message': 'Книга успешно возвращена в библиотеку'}), 200


@app.route('/books/search')
def search_books():
    search_string = request.args.get('query')

    books = session.query(Book).filter(
        Book.name.ilike(f"%{search_string}%")).all()
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


@app.route('/books/remaining', methods=['GET'])
def get_remaining_books():
    author_id = request.args.get('author_id')

    if not author_id:
        return jsonify({'error': 'Missing author_id parameter'}), 400

    author = session.query(Author).filter_by(id=author_id).first()

    if not author:
        return jsonify({'error': 'Author not found'}), 404

    books = session.query(Book).filter_by(author_id=author_id).all()
    total_count = sum([book.count for book in books])
    available_count = sum([book.count for book in books if book.count > 0])

    return jsonify({
        'author': {'id': author.id, 'name': author.name, 'surname': author.surname},
        'total_count': total_count,
        'available_count': available_count
    })


@app.route('/books/unread', methods=['GET'])
def get_unread_books():
    student_id = request.args.get('student_id')

    if not student_id:
        return jsonify({'error': 'Missing student_id parameter'}), 400

    student = session.query(Student).filter_by(id=student_id).first()

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    borrowed_books = [receiving_book.book_id for receiving_book in student.receiving_books]
    unread_books = session.query(Book).filter(
        Book.author_id.in_([book.author_id for book in student.receiving_books if book.book_id not in borrowed_books])
    ).all()

    unread_book_list = [{
        'id': book.id,
        'name': book.name,
        'count': book.count,
        'release_date': book.release_date,
        'author_id': book.author_id
    } for book in unread_books]

    return jsonify(unread_book_list)


@app.route('/books/average-borrowed', methods=['GET'])
def get_average_borrowed_books():
    current_date = datetime.now()
    current_month = current_date.month

    borrowed_books = session.query(ReceivingBook).filter(
        extract('month', ReceivingBook.date_of_issue) == current_month
    ).all()

    average_books = len(borrowed_books) / len(set([book.student_id for book in borrowed_books]))

    return jsonify({'average_borrowed_books': average_books})


@app.route('/books/most-popular', methods=['GET'])
def get_most_popular_book():
    students = session.query(Student).filter(Student.average_score > 4.0).all()

    student_ids = [student.id for student in students]

    most_popular_book = session.query(ReceivingBook.book_id, func.count(ReceivingBook.book_id)).\
        filter(ReceivingBook.student_id.in_(student_ids)).\
        group_by(ReceivingBook.book_id).\
        order_by(func.count(ReceivingBook.book_id).desc()).\
        first()

    if most_popular_book:
        book_id, count = most_popular_book
        book = session.query(Book).get(book_id)
        return jsonify({'most_popular_book': book.serialize()})
    else:
        return jsonify({'most_popular_book': None})


@app.route('/students/top-readers', methods=['GET'])
def get_top_readers():
    current_year = datetime.now().year

    top_readers = session.query(Student).\
        join(ReceivingBook).\
        filter(ReceivingBook.date_of_issue >= datetime(current_year, 1, 1)).\
        group_by(Student.id).\
        order_by(desc(func.count(ReceivingBook.id))).\
        limit(10).\
        all()

    if top_readers:
        top_readers_list = [student.serialize() for student in top_readers]
        return jsonify({'top_readers': top_readers_list})
    else:
        return jsonify({'top_readers': []})


@app.route('/students/upload', methods=['POST'])
def upload_students():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename.endswith('.csv'):
        reader = csv.DictReader(file, delimiter=';')

        students_data = []
        for row in reader:
            student_data = {
                'name': row['name'],
                'surname': row['surname'],
                'phone': row['phone'],
                'email': row['email'],
                'average_score': float(row['average_score']),
                'scholarship': bool(int(row['scholarship']))
            }
            students_data.append(student_data)

        # Массовая вставка данных студентов в базу данных
        session.bulk_insert_mappings(Student, students_data)
        session.commit()

        return jsonify({'message': 'Students uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format. Expected CSV file'}), 400


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
