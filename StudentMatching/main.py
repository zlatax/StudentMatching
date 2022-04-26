from flask import Blueprint, render_template, redirect, url_for, session

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route("/login", methods=['post', 'get'])
def login():
    if request.method == "POST":
        user = request.form["inputEmail"]
        session['user'] = user
        return redirect(url_for("user"))
    else:
        return render_template("login.html")
    
@main.route("/signup", methods=['post', 'get'])
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