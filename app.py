import sqlite3
from flask import Flask, render_template, redirect, url_for
import subprocess
import sys

app = Flask(__name__)

DB_NAME = "database.db"


def get_dashboard_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT position,
               movie_name,
               weekend_gross,
               total_gross,
               weeks_open
        FROM movies
        ORDER BY position ASC
    """)

    movies = cursor.fetchall()
    conn.close()

    total_movies = len(movies)

    top_movie = movies[0][1] if total_movies else "N/A"
    top_weekend = movies[0][2] if total_movies else "$0M"

    def clean_amount(value):
        try:
            value = value.replace("$", "").replace("M", "")
            return float(value)
        except:
            return 0

    chart_labels = [m[1] for m in movies]
    chart_weekend_values = [clean_amount(m[2]) for m in movies]
    chart_total_values = [clean_amount(m[3]) for m in movies]

    return {
        "movies": movies,
        "total_movies": total_movies,
        "top_movie": top_movie,
        "top_weekend": top_weekend,
        "chart_labels": chart_labels,
        "chart_weekend_values": chart_weekend_values,
        "chart_total_values": chart_total_values,
    }


@app.route("/")
def home():
    data = get_dashboard_data()
    return render_template("dashboard.html", **data)


@app.route("/analytics")
def analytics():
    data = get_dashboard_data()
    return render_template(
        "analytics.html",
        **data
    )

@app.route("/database")
def database():
    data = get_dashboard_data()
    return render_template(
        "database.html",
        **data
    )


@app.route("/refresh")
def refresh():
    try:
        # Uses the same Python interpreter running Flask
        subprocess.run([sys.executable, "scraper.py"], check=True)
    except Exception as e:
        return f"Scraper Error: {e}"

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)