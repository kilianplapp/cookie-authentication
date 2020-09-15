import flask, json, flask_wtf, time, uuid
from flask import Flask, render_template, request, redirect, url_for, make_response
app = Flask(__name__)
users = {"testaccount1":"password","testaccount2":"password"}
validtoken = {}
tokencreationtime = {}
sessionlength = 15
@app.route('/')
def login():
    return render_template("index.html")
@app.route('/login', methods = ['POST', 'GET'])
def setcookie():
    username = request.args["uname"]
    password = request.args["pword"]
    for i in users:
        if(i != username): continue
        if(users[i] != password): return redirect("/error?c=401")
        if(request.method == 'GET'):
            global validtoken, tokencreationtime
            tokencreationtime.update({str(username):int(time.time())})
            validtoken.update({str(username):str(uuid.uuid4())})
            resp = make_response(redirect('home'))
            resp.set_cookie('token', validtoken[username])
            return resp
    return redirect("/error?c=401")
@app.route('/home')
def getcookie():
    name = request.cookies.get('token')
    for i in validtoken:
        if(str(validtoken[i]) != str(name)): continue     
        if(int(tokencreationtime[i]) + sessionlength < int(time.time())): return redirect("/")
        timeleft = int(tokencreationtime[i] - int(time.time()) + sessionlength)
        return render_template("login.html",username=i,timeleft=timeleft)
    return redirect("/")        
@app.route('/error')
def errorpage():
    try: error = request.args["c"]
    except: error = None
    if(error == '401'): return "<h1>ERROR: 401</h1><p>Missing or incorrect credentials</p>"
    return "<h1>ERROR</h1><p>An unspecified error occured</p>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

