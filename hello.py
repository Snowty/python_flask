from flask import Flask, render_template,session,redirect,url_for,flash,request,\
    current_app
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Required,IPAddress
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
import os,datetime,time

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


class PostForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    hostname = StringField('Hostname', validators=[Required()])
    ip = StringField('IP',validators=[IPAddress()])
    package = StringField('Package', validators=[Required()])
    language = StringField('Language', validators=[Required()])
    time = StringField('Time', validators=[Required()])
    submit = SubmitField('Submit')

def make_shell_context():
    return dict(app=app,db=db,User=User)
manager.add_command("shell",Shell(make_context=make_shell_context))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64))
    hostname = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    package = db.Column(db.String(64))
    language = db.Column(db.String(64))
    time = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime,index=True)

    def __repr__(self):
        return '<User %r>'% self.username

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    page = request.args.get('page',1,type=int)
    pagination = User.query.order_by(User.timestamp.desc()).paginate(page,error_out=False)
    users = pagination.items
    #users = User.query.all()
    return render_template('index.html',users = users,pagination=pagination)


@app.route('/p/',strict_slashes=False, methods=['GET', 'POST'])
def user():
    form = PostForm()
    if form.validate_on_submit():
        u = User(username = form.username.data,hostname = form.hostname.data,ip = form.ip.data,package = form.package.data,language = form.language.data,time = form.time.data)
        db.session.add(u)
        db.session.commit()
        #return redirect(url_for('index'))
    return render_template('postpage.html', form=form)


if __name__ == '__main__':
    manager.run()
