from flask import Flask, request, render_template, jsonify, send_from_directory
import pandas as pd
from sqlalchemy import create_engine
import subprocess

app = Flask(__name__)

@app.route('/run_crawl')
def run_crawl():
    name = request.args.get('name', '')
    subprocess.run(['python', 'app.py', name], check=True)
    return jsonify({'status': 'done'})

@app.route('/search')
def search():
    name = request.args.get('name', '')
    engine = create_engine("mysql+pymysql://root:1234@localhost:3306/finy")
    # f-string으로 쿼리문 만들기 (params 사용 X)
    query = f"SELECT * FROM item WHERE Name LIKE '%%{name}%%'"
    df = pd.read_sql(query, con=engine)
    return render_template('search.html', items=df.to_dict(orient='records'), keyword=name)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)