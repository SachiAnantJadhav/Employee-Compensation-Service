import os
import mssql_python


def get_connection():
    connection_string = os.environ["DATABASE_CONNECTION_STRING"]

    return mssql_python.connect(
        connection_string,
        timeout=60
    )