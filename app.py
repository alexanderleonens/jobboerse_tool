from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)

#shows index file once app.py gets executed
@app.route('/')
def index():
	return render_template('index.html')

#mock function "sends" a request to Sugar CRM and checks wether user is a company
def valid_company_login(username,password):
	if(username=="a" and password=="b"):
        #session["token"] = username;
		return True

#working function sends a request to Amiv API and checks wether user is boardmember or Kontakt
def valid_admin_login(user,password):
    #starts session return is a number
    resp = requests.post('http://192.168.1.100/sessions', data={'username':'user0','password':'user0'})
    if resp.status_code == 201:
        #parse return to a JSON object out of whichwe get information for the session and user
        resp_parsed = resp.json()
        user_id = resp_parsed['user']
        user_token = resp_parsed['token']
        #send request to check in which groups the user is and ("embedded") displays full group information
        groupmember_status = requests.get('http://192.168.1.100/groupmemberships?where={"user": "%s"}&embedded={"group":1}' % user_id, headers={'Authorization':user_token})
        groupmember_parsed = groupmember_status.json()
        print (groupmember_parsed)
        #loops through different groups and checks wether one is Vorstand or Kontakt
        for group_obj in groupmember_parsed['_items']:
            print (group_obj)
            if group_obj['group']['name'] == 'Vorstand' or group_obj['group']['name'] == 'Kontakt':
                return True
    return False

@app.route('/login', methods=['GET','POST'])
def authenticate():
    error = None
    if request.method == 'POST':
        #first check wether user is a company
        if valid_company_login(request.form['username'],
                       request.form['password']):
            return render_template('submitJobForm.html')
        #else check wether user is Amiv boardmember or Kontakt OK
        elif valid_admin_login(request.form['username'],
                       request.form['password']):
            return render_template('submitJobForm.html')
        else:
            error = 'Invalid username/password'
            return error 
    else:
        return "Wrong request"


#makes it possible to run program in terminal
if __name__ == "__main__":
	app.run()