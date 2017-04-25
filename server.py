from flask import *
from models import User
import sqlite3 as sql
from hashlib import sha1

users = []
db_path = "database/database.db"
app = Flask(__name__, template_folder="views")


@app.before_request
def before_request():
	index = session.get("user")
	if index >= 0 and index >= len(users):
		session.clear()
		return redirect(url_for("index"))


@app.route("/")
def index():
	index = session.get("user")
	if index >= 0:
		user = users[index]
		return render_template("index.jinja2", user=user)
	else:
		return render_template("index.jinja2")


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "GET":
		return render_template("login.jinja2")
	else:
		try:
			with sql.connect(db_path) as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM Users WHERE Email=? AND Password=?",
							(request.form["email"], str(sha1(request.form["password"]).hexdigest())))
				rows = cur.fetchall()
				if len(rows) > 0:
					user = User(*rows[0])
					users.append(user)
					session["user"] = users.index(user)
					return redirect(url_for("index"))
				else:
					return render_template("login.jinja2", message="Invalid username or password!")
		except:
			con.rollback()
			print "error in select operation"
		finally:
			con.close()


@app.route("/register", methods=["POST", "GET"])
def register():
	if request.method == "GET":
		return render_template("register.jinja2")
	else:
		try:
			with sql.connect(db_path) as con:
				cur = con.cursor()
				cur.execute("INSERT INTO Users (Firstname, Lastname, Email, Password) VALUES(?, ?, ?, ?)", (
					request.form["firstname"], request.form["lastname"], request.form["email"], str(sha1(request.form["password"]).hexdigest())))
		except:
			con.rollback()
			print "error in insert operation"
		finally:
			con.close()
			return redirect(url_for("login"))


@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for("index"))


if __name__ == "__main__":
	app.config["TEMPLATES_AUTO_RELOAD"] = True
	app.secret_key = "secret is her!"
	app.run(debug=True, host="0.0.0.0")
