from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask instance
app = Flask(__name__)

# Add database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = "sweetie-pie"

# Initialize database
db = SQLAlchemy(app)

# Create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a form class
class Form(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")



posts = [
    {"title": "First Post", "author": "Author 1", "content": "This is the content of the first post."},
    {"title": "Second Post", "author": "Author 2", "content": "This is the content of the second post."},
    {"title": "Third Post", "author": "Author 3", "content": "This is the content of the third post."},
    {"title": "Fourth Post", "author": "Author 4", "content": "This is the content of the fourth post."}
]

# Create routes
@app.route('/')
def index():
    return render_template('index.html', posts =posts)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = Form()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully!")
    return render_template("name.html", name=name, form=form)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)
