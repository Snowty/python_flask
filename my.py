from flask import Flask,render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)



@app.route('/pp/')
def index():
    return render_template('index.html')


@app.route('/')
def user():
    return render_template('act.html')

if __name__ == '__main__':
    manager.run()
