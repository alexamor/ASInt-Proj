from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/add_secretariat')
def add_secretariat():
    return render_template('add_secretariat.html')

@app.route('/canteen')
def canteen():
    return render_template('canteen.html')


@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/qr')
def qr():
    return render_template('qr.html')


if __name__ == '__main__':
    app.run()


