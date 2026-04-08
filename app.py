from flask import Flask, render_template, request, redirect, session, send_file
import os
import matplotlib.pyplot as plt

from model import rank_resumes
from auth import login_user, signup_user


app = Flask(__name__)
app.secret_key = "secret"


UPLOAD_FOLDER = "resumes"
JD_FOLDER = "jd"
RESULT_FOLDER = "results"
STATIC_FOLDER = "static"


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(JD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = request.form["username"]
        pw = request.form["password"]

        if login_user(user, pw):

            session["user"] = user
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        user = request.form["username"]
        pw = request.form["password"]

        signup_user(user, pw)

        return redirect("/")

    return render_template("signup.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        jd_file = request.files["jd"]
        resumes = request.files.getlist("resumes")

        jd_path = os.path.join(JD_FOLDER, jd_file.filename)
        jd_file.save(jd_path)

        resume_paths = []

        for r in resumes:
            path = os.path.join(UPLOAD_FOLDER, r.filename)
            r.save(path)
            resume_paths.append(path)

        result = rank_resumes(jd_path, resume_paths)

        result_path = os.path.join(
            RESULT_FOLDER,
            "result.csv"
        )

        result.to_csv(result_path, index=False)

        # charts

        bar_path = os.path.join(STATIC_FOLDER, "bar.png")
        pie_path = os.path.join(STATIC_FOLDER, "pie.png")
        top_path = os.path.join(STATIC_FOLDER, "top.png")

        # bar

        plt.figure()
        plt.bar(result["Resume"], result["Score (%)"])
        plt.savefig(bar_path)
        plt.close()

        # pie

        plt.figure()
        plt.pie(
            result["Score (%)"],
            labels=result["Resume"],
            autopct="%1.1f%%"
        )
        plt.savefig(pie_path)
        plt.close()

        # top 3

        top3 = result.head(3)

        plt.figure()
        plt.bar(top3["Resume"], top3["Score (%)"])
        plt.savefig(top_path)
        plt.close()

        top_candidate = result.iloc[0]["Resume"]
        total_resumes = len(result)

        return render_template(
            "result.html",
            tables=result.to_html(
                classes="table table-striped",
                index=False
            ),
            bar="static/bar.png",
            pie="static/pie.png",
            top="static/top.png",
            top_candidate=top_candidate,
            total=total_resumes
        )

    return render_template("dashboard.html")


@app.route("/download")
def download():

    return send_file(
        "results/result.csv",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)