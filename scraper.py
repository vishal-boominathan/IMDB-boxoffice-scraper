import sqlite3
from playwright.sync_api import sync_playwright

DB_NAME = "database.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            position INTEGER PRIMARY KEY,
            movie_name TEXT,
            weekend_gross TEXT,
            total_gross TEXT,
            weeks_open TEXT
        )
    """)

    conn.commit()
    conn.close()


def scrape():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM movies")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(
            "https://www.imdb.com/chart/boxoffice",
            wait_until="domcontentloaded"
        )

        page.wait_for_selector(
    "li.ipc-metadata-list-summary-item",
    timeout=30000
)

        cards = page.locator("li.ipc-metadata-list-summary-item")

        count = cards.count()

        print("Found", count, "movies")

        for i in range(min(10, count)):

            card = cards.nth(i)

            lines = [
                x.strip()
                for x in card.inner_text().split("\n")
                if x.strip()
            ]

            title = lines[0]

            weekend = "N/A"
            total = "N/A"
            weeks = "N/A"

            for line in lines:

                if line.startswith("Weekend Gross"):
                    weekend = line.replace("Weekend Gross:", "").strip()

                elif line.startswith("Total Gross"):
                    total = line.replace("Total Gross:", "").strip()

                elif line.startswith("Weeks Released"):
                    weeks = line.replace("Weeks Released:", "").strip()

            cur.execute(
                """
                INSERT INTO movies
                VALUES(?,?,?,?,?)
                """,
                (
                    i + 1,
                    title,
                    weekend,
                    total,
                    weeks
                )
            )

            print(i + 1, title)

        conn.commit()
        conn.close()

        browser.close()

        print("Database Updated Successfully")


if __name__ == "__main__":
    init_db()
    scrape()