from flask import Flask, render_template, redirect
import sqlite3
from scraper import scrape, init_db

app = Flask(__name__)

DB_NAME = "database.db"


def get_movies():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT position,
               movie_name,
               weekend_gross,
               total_gross,
               weeks_open
        FROM movies
        ORDER BY position
    """)

    movies = cur.fetchall()

    conn.close()

    return movies


@app.route("/")
def index():
    movies = get_movies()
    return render_template("index.html", movies=movies)


@app.route("/refresh")
def refresh():

    init_db()
    scrape()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)