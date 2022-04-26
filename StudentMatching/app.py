from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from dotenv import dotenv_values

config=dotenv_values(".env")

app = Flask(__name__)
app.secret_key="hello"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

client = PyMongo()

# client = MongoClient(config['MONGO_URL'])
# db = client.get_database('StudentMatcher')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username="Thong", matched_friends=matched_friends)

@app.route("/login", methods=['post', 'get'])
def login():
    if request.method == "POST":
        user = request.form["inputEmail"]
        session['user'] = user
        return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}<h1>"
    else:
        return redirect(url_for("login"))

    # pass
    # message = ''
    # if "email" in session:
    #     return redirect(url_for("dashboard"))
    # if request.method == "POST":
    #     email = request.form.get("inputEmail")

    #     password1 = request.form.get("inputPassword")

    #     email_found = records.find_one({"email": email})
    #     if email_found:


    #         message = 'This email already exists in database'
    #         return render_template('login.html', message=message)
    #     if password1 != password2:
    #         message = 'Passwords should match!'
    #         return render_template('login.html', message=message)
    #     else:
    #         hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
    #         user_input = {'name': user, 'email': email, 'password': hashed}
    #         records.insert_one(user_input)
            
    #         user_data = records.find_one({"email": email})
    #         new_email = user_data['email']
   
    #         return render_template('dashboard.html', email=new_email)
    # return render_template('login.html')

@app.route("/signup", methods=['post', 'get'])
def signup():
    message = ''
    if "email" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("inputEmail")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_found = records.find_one({"email": email})
        if email_found:
            message = 'This email already exists in database'
            return render_template('login.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('login.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('dashboard.html', email=new_email)
    return render_template('login.html')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)