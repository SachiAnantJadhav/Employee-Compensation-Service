import json
import os

from src.database.connection import get_connection


def load_local_settings():
    with open("local.settings.json", "r") as file:
        settings = json.load(file)

    for key, value in settings["Values"].items():
        os.environ[key] = value


def main():
    load_local_settings()

    connection = get_connection()

    cursor = connection.cursor()
    cursor.execute("SELECT 1 AS TestValue")

    row = cursor.fetchone()

    print("Database connection successful!")
    print("Result:", row[0])

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()