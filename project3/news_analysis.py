#!/usr/bin/env python3
import psycopg2


def execute_query(query):
    """This function connects to the news database and
    executes the SQL query that was passed to the function as a string"""

    try:
        db = psycopg2.connect(database="news")
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        db.close()
        return rows
    except:
        print("Unable to execute query")


def top_articles():
    """This function queries the news database to find the
    3 most viewed articles of all time"""

    query = (
        "SELECT title, COUNT(*) "
        "FROM log JOIN articles "
        "ON RIGHT(path, LENGTH(path) - 9) = slug "
        "WHERE status LIKE '%200%' "
        "GROUP BY title "
        "ORDER BY 2 DESC "
        "LIMIT 3")
    rows = execute_query(query)

    # Print the question and the top articles on seperate lines
    print("\nWhat are the most popular three articles of all time?")
    for row in rows:
        print("  '{}' - {} views".format(row[0], row[1]))


def top_authors():
    """This function queries the news database to find the
    authors with the most views"""

    query = (
        "SELECT authors.name, COUNT(*) "
        "FROM log JOIN articles "
        "ON RIGHT(path, LENGTH(path) - 9) = slug "
        "JOIN authors ON articles.author = authors.id "
        "WHERE status LIKE '%200%' "
        "GROUP BY authors.name "
        "ORDER BY 2 DESC")
    rows = execute_query(query)

    # Print the question and the top authors on seperate lines
    print("\nWho are the most popular article authors of all time?")
    for row in rows:
        print("  {} - {} views".format(row[0], row[1]))


def errors_over_one_percent():
    """This function queries the news database to find
    days that had errors on more than 1% of requests"""

    query = (
        "SELECT CAST(time AS Date), 100.0 "
        "* SUM(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) "
        "/ COUNT(*) "
        "FROM log "
        "GROUP BY CAST(time AS Date) "
        "HAVING 100.0 "
        "* SUM(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) "
        "/ COUNT(*) > 1 "
        "ORDER BY 1")
    rows = execute_query(query)

    # Print the question and the error-filled days on seperate lines
    print("\nOn which days did more than 1% of requests lead to errors?")
    for row in rows:
        print("  {} - {}% errors\n"
              .format(row[0].strftime("%B %d, %Y"), round(row[1], 2)))

# Ensure the program is run directly from the terminal
if __name__ == "__main__":
    top_articles()
    top_authors()
    errors_over_one_percent()
