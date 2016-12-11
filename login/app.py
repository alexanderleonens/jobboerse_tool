from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def valid_company_login(username,password):
	if(username=="a" and password=="b"):
        #session["token"] = username;
		return True

def valid_admin_login(user,password):
    resp = requests.post('http://192.168.1.100/sessions', data={'username':'user0','password':'user0'})
    if resp.status_code == 201:
        resp_parsed = resp.json()
        user_id = resp_parsed['user']
        user_token = resp_parsed['token']
        groupmember_status = requests.get('http://192.168.1.100/groupmemberships?where={"user": "%s"}&embedded={"group":1}' % user_id, headers={'Authorization':user_token})
        groupmember_parsed = groupmember_status.json()
        print (groupmember_parsed)
        for group_obj in groupmember_parsed['_items']:
            print (group_obj)
            if group_obj['group']['name'] == 'Vorstand' or group_obj['group']['name'] == 'Kontakt':
                return True
    return False

@app.route('/login', methods=['GET','POST'])
def authenticate():
    error = None
    if request.method == 'POST':
        if valid_company_login(request.form['username'],
                       request.form['password']):
            return render_template('submitJobForm.html')
        elif valid_admin_login(request.form['username'],
                       request.form['password']):
            return render_template('submitJobForm.html')
        else:
            error = 'Invalid username/password'
            return error 
    else:
        return "Wrong request"



if __name__ == "__main__":
	app.run()