from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_session import Session
from datetime import timedelta
from utils.database import Database
import os



app = Flask(__name__)
db = Database()


app.secret_key = "zaBMssQvjFGHtFdfsjolpu"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

Session(app)

@app.before_request
def redirect_https():
    if os.environ.get('DYNO'):
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        passwd = data.get('passwd')

        callcenterid = db.get_callcenter_id(email, passwd)
        print(callcenterid)
        if callcenterid != None:
            session['callcenterid'] = callcenterid
            return jsonify({'status': 'yes'})
        else:
            return jsonify({'status': 'no'})
    else:  
        return render_template('index.html')





@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/', methods=['GET'])
def index():
    if 'callcenterid' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if 'callcenterid' in session:
            return render_template('home.html')
    else:#post
        if 'callcenterid' in session:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
        


#if __name__ == '__main__':
    #app.run(port=8181, host="0.0.0.0")
    #app.run(debug=True)
    #app.run()    pass
