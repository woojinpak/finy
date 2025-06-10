from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''<!doctype html>
    <html>
        <body>
            hello
        </body>
    </html>




    '''

app.run(debug=True)
