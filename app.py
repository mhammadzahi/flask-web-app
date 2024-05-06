from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_session import Session
from datetime import timedelta
from utils.database import Database
import os


app = Flask(__name__)
db = Database()


app.secret_key = "zaBMsssQvjFGHtFfsjolpu"
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



@app.route('/call-center-login', methods=['POST', 'GET'])
def callcenter_login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        passwd = data.get('passwd')

        call_center_id = db.get_callcenter_id(email, passwd)
        
        if call_center_id != None:
            session['call_center_id'] = call_center_id
            return jsonify({'status': 'yes'})
        else:
            return jsonify({'status': 'no'})
    else:#get
        return render_template('call-center-login.html')



@app.route('/agent-login', methods=['POST', 'GET'])
def agent_login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        passwd = data.get('passwd')

        agent_id = db.get_agent_id(email, passwd)

        if agent_id != None:
            session['agent_id'] = agent_id
            return jsonify({'status': 'yes'})
        else:
            return jsonify({'status': 'no'})
    else: # GET
        return render_template('agent-login.html')



@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/', methods=['GET'])
def index():
    if 'call_center_id' in session:
        return render_template('call-center-home.html')

    elif 'agent_id' in session:
        return render_template('agent-home.html')

    else:
        return render_template('index.html')



@app.route('/call-center-home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if 'call_center_id' in session:
            return render_template('home.html')
    else:#post
        if 'call_center_id' in session:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))



if __name__ == '__main__':
    #app.run(port=8181, host="0.0.0.0")
    app.run(debug=True)
    #app.run()    pass
