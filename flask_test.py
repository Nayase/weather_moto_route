from flask import Flask
app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/')
def index():
    return app.send_static_file('input.html')

@app.route('/hello/<name>')
def hello(name):
    return name

app.run(port=8000, debug=True)