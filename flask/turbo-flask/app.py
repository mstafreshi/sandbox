from flask import Flask, render_template, flash, redirect, url_for, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from turbo_flask import Turbo
import time
import os
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = "hard-to-guess-value"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "db.sqlite")
db = SQLAlchemy(app)
migrate = Migrate(app, db)      
turbo = Turbo(app)

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_data).start()   

def update_data():
    counter = 0
    with app.app_context():
        while True:            
            turbo.push(turbo.update(render_template('runtime.html', counter=counter), 'runtime'))
            counter += 1
            time.sleep(1)
            
@app.route("/", methods=["GET", "POST"])
def index():
    form = RegisterForm()
    if form.is_submitted():
        user = None
        if form.id.data:
            user = User.query.get(int(form.id.data))
        if user is None:
            user = User()
        if form.validate():
            user.username=form.username.data
            db.session.add(user)
            db.session.commit()
            
            flash("User registered/editted successfully.", category='success')            
        response = make_response(render_template("register_result.html", user=user, form=form))
        response.headers['Content-type'] = 'text/vnd.turbo-stream.html'
        return response
        
    users = User.query.order_by(User.id.desc()).all()           
    return render_template("index.html", form=form, users=users)
 
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tests")
def tests():
    return render_template("tests.html")

@app.route("/delete/<int:id>", methods=["DELETE"]) 
def delete(id):
    user = User.query.get(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
                
        turbo.push(turbo.remove("user_"+str(id)))
    return '<turbo-frame id="delete_result"><div class="alert alert-danger">Deleted successfully</div></turbo-frame>'
            
@app.route("/edit_user/<int:id>")
def edit_user_form(id):
    user = User.query.get(id)
    form = RegisterForm(obj=user)
    txt = render_template("user_form.html", form=form)
    txt = '<turbo-stream action="update" target="user_{id}"><template>'+txt+'</template></turbo-stream>'
    txt = txt.format(id=id)
            
    response = make_response(txt)
    response.headers['Content-type'] = 'text/vnd.turbo-stream.html'
    return response     
    
@app.route("/eager_loading")
def eager_loading():
    time.sleep(5)
    return "<turbo-frame id='eager_loading'><h3>Page loaded</h3></turbo-frame>"
     
class RegisterForm(FlaskForm):
    id = HiddenField("Id")
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Register")
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username taken")
 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
                   
if __name__ == "__main__":
    app.run()            
