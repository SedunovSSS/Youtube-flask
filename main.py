from models import *


@app.route('/')
def main():
    name = request.cookies.get('user')
    search = request.args.get("search")
    if search is None:
        videos = Videos.query.all()
    elif search == "":
        videos = Videos.query.all()
    else:
        videos = Videos.query.filter_by(title=search).all()
    if len(videos) > 2:
        videos = list(reversed(videos))
    elif len(videos) == 2:
        videos[0], videos[1] = videos[1], videos[0]
    else:
        videos = list(videos)
    if name is None:
        name = "Guest"
    try:
        path = db.session.query(Users.path).filter_by(login=name).first()[0]
        if videos is not None:
            return render_template("index.html", name=name, path=path, videos=videos)
        else:
            return render_template("index.html", name=name, path=path)
    except:
        if videos is not None:
            return render_template("index.html", name=name, videos=videos)
        else:
            return render_template("index.html", name=name)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        login = request.form['login']
        email = request.form['email']
        passw1 = request.form['passw1']
        passw2 = request.form['passw2']
        file = request.files['icon[]']
        path = ""

        if passw1 == passw2:
            password = hashlib.md5(passw1.encode("utf-8")).hexdigest()
            exists = db.session.query(Users.id).filter_by(login=login).first() is not None or db.session.query(Users.id).filter_by(email=email).first() is not None
            if not exists:
                if file:
                    path = f"static/uploads/{login}"
                    if not os.path.exists(path):
                        os.makedirs(path)
                    if not os.path.exists(path + "/icon.png"):
                        file.save(f"static/uploads/{login}/icon.png")
                user = Users(login=login, email=email, password=password, path=str(path+"/icon.png"))
            else:
                return redirect("/register")
            try:
                db.session.add(user)
                db.session.commit()
                resp = make_response(redirect("/"))
                resp.set_cookie('user', user.login)
                return resp
            except Exception as ex:
                print(ex)
                return redirect("/register")
    else:
        name = request.cookies.get('user')
        if name is None:
            name = "Guest"
        try:
            path = db.session.query(Users.path).filter_by(login=name).first()[0]
            return render_template("register.html", name=name, path=path)
        except:
            return render_template("register.html", name=name)


@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        passw1 = request.form['passw1']
        passw2 = request.form['passw2']
        if passw1 == passw2:
            password = hashlib.md5(passw1.encode("utf-8")).hexdigest()
            exists = db.session.query(Users.id).filter_by(email=email, password=password).first() is not None
            user = db.session.query(Users.login).filter_by(email=email, password=password).first()
            if exists:
                resp = make_response(redirect("/"))
                resp.set_cookie('user', user[0])
                return resp
            else:
                return redirect("/login")

        else:
            name = request.cookies.get('user')
            if name is None:
                name = "Guest"
            try:
                path = db.session.query(Users.path).filter_by(login=name).first()[0]
                return render_template("login.html", name=name, path=path)
            except:
                return render_template("login.html", name=name)
    else:
        name = request.cookies.get('user')
        if name is None:
            name = "Guest"
        try:
            path = db.session.query(Users.path).filter_by(login=name).first()[0]
            return render_template("login.html", name=name, path=path)
        except:
            return render_template("login.html", name=name)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        email = request.form['email']
        passw1 = request.form['passw1']
        passw2 = request.form['passw2']
        file = request.files['icon[]']
        login = request.cookies.get("user")
        if file:
            path = f"static/uploads/{login}"
            file.save(f"{path}/icon.png")
        if passw1 == passw2:
            name = request.cookies.get('user')
            password = hashlib.md5(passw1.encode("utf-8")).hexdigest()
            if name is not None:
                user = Users.query.filter_by(login=name).first()
                try:
                    path = f"static/uploads/{login}/icon.png"
                    user.email = email
                    if not passw1 == "" or not passw2 == "":
                        print(passw1, passw2)
                        user.password = password
                    else:
                        return redirect("/profile")
                    user.path = path
                    db.session.commit()
                    return redirect("/")
                except:
                    return redirect("/profile")
            else:
                return redirect("/login")
    else:
        name = request.cookies.get('user')
        if name is not None:
            email = db.session.query(Users.email).filter_by(login=name).first()[0]
            path = db.session.query(Users.path).filter_by(login=name).first()[0]
            return render_template("profile.html", name=name, path=path, login=name, email=email)
        else:
            return 'None'


@app.route('/admin')
def admin():
    name = request.cookies.get('user')
    if name in admins:
        users = Users.query.all()
        try:
            path = db.session.query(Users.path).filter_by(login=name).first()[0]
            return render_template("admin.html", name=name, path=path, users=users, length=len(users))
        except:
            return redirect("/")
    else:
        return redirect("/")


@app.route('/admin/changeuser', methods=['GET', 'POST'])
def admin_change_user():
    if request.method == "POST":
        email = request.form['email']
        passw1 = request.form['passw1']
        passw2 = request.form['passw2']
        file = request.files['icon[]']
        login = request.args.get('user')
        if file:
            path = f"static/uploads/{login}"
            file.save(f"{path}/icon.png")
        if passw1 == passw2:
            password = hashlib.md5(passw1.encode("utf-8")).hexdigest()
            if login is not None:
                user = Users.query.filter_by(login=login).first()
                try:
                    path = f"static/uploads/{login}/icon.png"
                    user.email = email
                    user.password = password
                    if file:
                        user.path = path
                    db.session.commit()
                    return redirect("/admin")
                except Exception as ex:
                    print(ex)
                    return redirect("/admin")
            else:
                return redirect("/admin")
    else:
        name = request.cookies.get('user')
        user_login = request.args.get('user')
        if name in admins:
            user = Users.query.filter_by(login=user_login).first()
            path = db.session.query(Users.path).filter_by(login=name).first()[0]
            return render_template("changeuser.html", user=user, name=name, path=path)
        else:
            return redirect("/")


@app.route("/admin/deluser", methods=['GET'])
def admin_del_user():
    name = request.cookies.get('user')
    if name in admins:
        login = request.args.get('user')
        path = db.session.query(Users.path).filter_by(login=login).first()[0]
        os.remove(path)
        Users.query.filter_by(login=login).delete()
        db.session.commit()
        return redirect("/admin")
    else:
        return redirect("/")


@app.route("/addvideo", methods=['GET', 'POST'])
def addvideo():
    if request.method == "POST":
        author = request.cookies.get("user")
        title = request.form['title']
        description = request.form['description']
        image = request.files['image[]']
        video = request.files['video[]']
        video.filename = str(video.filename).replace(" ", "_").replace(":", "_")
        t = title
        p = f"static/uploads/{author}/{t}"
        path = f"static/uploads/{author}/{t}/{video.filename}"
        preview_path = f"static/uploads/{author}/{t}/{image.filename}"
        image.filename = str(image.filename).replace(" ", "_").replace(":", "_")
        while os.path.exists(p):
            t = "exists123" + t
            p = f"static/uploads/{author}/{t}"
            path = f"static/uploads/{author}/{t}/{video.filename}"
            preview_path = f"static/uploads/{author}/{t}/{image.filename}"
        os.makedirs(p)
        if video and image:
            video.save(path)
            image.save(preview_path)
            video = Videos(title=title, t=t, description=description, path=path, author=author, preview_path=preview_path)
        else:
            return redirect("/addvideo")
        try:
            if author is not None and title is not None:
                db.session.add(video)
                db.session.commit()
                return redirect("/")
            else:
                return redirect("/addvideo")
        except Exception as ex:
            print(ex)
            return redirect("/addvideo")
    else:
        name = request.cookies.get('user')
        if name is not None:
            try:
                path = db.session.query(Users.path).filter_by(login=name).first()[0]
                return render_template("addvideo.html", name=name, path=path)
            except:
                return redirect("/")
        else:
            return redirect("/login")


@app.route("/watch", methods=['GET', 'POST'])
def watch():
    if request.method == "POST":
        post_id = request.args.get("id")
        author = request.cookies.get("user")
        text = request.form['comment']
        if author is not None:
            if post_id is not None and text is not None:
                comment = Comments(post_id=post_id, author=author, text=text)
                try:
                    db.session.add(comment)
                    db.session.commit()
                    return redirect(f"/watch?id={post_id}")
                except:
                    return redirect(f"/watch?id={post_id}")
            else:
                return redirect("/")
        else:
            return redirect("/login")
    else:
        id = request.args.get("id")
        name = request.cookies.get("user")
        path = db.session.query(Users.path).filter_by(login=name).first()[0]
        video = Videos.query.filter_by(id=id).first()
        video.watches += 1
        videos = Videos.query.filter_by(title=video.title).all()
        db.session.commit()
        if id is not None and path is not None:
            comments = Comments.query.filter_by(post_id=id).all()
            if len(comments) > 2:
                comments = list(reversed(comments))
            elif len(comments) == 2:
                comments[0], comments[1] = comments[1], comments[0]
            else:
                comments = list(comments)
            video = Videos.query.filter_by(id=id).first()
            return render_template("watch.html", video=video, videos=videos, name=name, path=path, comments=comments)
        else:
            return redirect("/")


@app.route("/myvideos", methods=['GET'])
def my_videos():
    name = request.cookies.get('user')
    video = Videos.query.filter_by(author=name).all()
    length = len(video)
    if name is None:
        name = "Guest"
    try:
        path = db.session.query(Users.path).filter_by(login=name).first()[0]
        if video is not None:
            return render_template("myvideos.html", name=name, path=path, video=video, length=length)
        else:
            return render_template("myvideos.html", name=name, path=path)
    except:
        if video is not None:
            return render_template("myvideos.html", name=name, video=video, length=length)
        else:
            return render_template("myvideos.html", name=name)


@app.route("/deletevideo")
def delete_video():
    name = request.cookies.get('user')
    id = request.args.get("id")
    video = Videos.query.filter_by(id=id, author=name).first()
    os.remove(video.path)
    os.remove(video.preview_path)
    os.rmdir(f"/static/uploads/{video.author}/{video.t}")
    Videos.query.filter_by(id=id, author=name).delete()
    db.session.commit()
    return redirect("/myvideos")


@app.route("/admin/videos")
def admin_videos():
    name = request.cookies.get("user")
    if name in admins:
        videos = Videos.query.all()
        path = db.session.query(Users.path).filter_by(login=name).first()[0]
        return render_template("adminvideos.html", videos=videos, length=len(videos), name=name, path=path)

    else:
        return redirect("/")


@app.route("/deletevideoadmin")
def delete_video_admin():
    name = request.cookies.get('user')
    if name in admins:
        id = request.args.get("id")
        video = Videos.query.filter_by(id=id).first()
        os.remove(video.path)
        os.remove(video.preview_path)
        os.rmdir(f"static/uploads/{video.author}/{video.t}")
        Videos.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect("/admin/videos")
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
