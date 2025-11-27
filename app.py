from flask import Flask, render_template, request, redirect, flash
import redis
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = "loc_demo_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Redis 
r = redis.Redis (
    host =os.getenv("REDIS_HOST"),
    port =int(os.getenv("REDIS_PORT", 6379)),
    password =os.getenv("REDIS_PASSWORD") or None,
    db =0 
)
@app.route("/")
def hello():

    # Redis test
    r.set('foo', 'bar')
    val = r.get('foo').decode('utf-8')

    return f"Hello Render! Redis: {val}"

# tạo bảng mẫu ở trong PostgreSQL
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# tạo giao diện HTML 
# Trang list user
@app.route("/web_users2/")
def web_users2():
    users = User.query.all()
    return render_template("users.html", users = users)

# Trang them user
@app.route("/add", methods = ["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        new_user = User(name = name)
        db.session.add(new_user)
        db.session.commit()
        flash("Thêm user thành công !")
        return redirect("/web_users2")

    return render_template("add.html")

# Trang sửa user
@app.route("/edit/<int:id>", methods = ["GET", "POST"])
def edit(id):
    user = User.query.get(id)

    if request.method == "POST":
        user.name = request.form["name"]
        db.session.commit()
        flash("Cập nhật user thành công!")
        return redirect("/web_users2")
    
    return render_template("edit.html", user = user)

# Trang xóa user
@app.route("/delete_user/<int:id>")
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Xóa user thành công!") 
    else:
        flash("User không tồn tại, hãy thử lại")
    return redirect("/web_users2")

@app.route("/init_db")
def init_db():
    try:
        with app.app_context():
            db.create_all()
        return "Database initallized!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)