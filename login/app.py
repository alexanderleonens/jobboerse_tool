from flask import Flask, render_template, request, session
from base64 import base64encode

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def valid_login(username,password):
	if(username=="a" and password=="b"):
        session["token"] = username;
		return True

@app.route('/login', methods=['GET','POST'])
def authenticate():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
#            return log_the_user_in(request.form['username'])
            return render_template('submitJobForm.html')
        else:
            error = 'Invalid username/password'
            return error 
    else:
        return "Wrong request"



if __name__ == "__main__":
	app.run()