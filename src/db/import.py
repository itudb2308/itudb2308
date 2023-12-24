import psycopg2


def run_sql(connection, file: str):
    cursor = connection.cursor()
    sql_statements = None

    with open(file) as f:
        sql_statements = f.read().split("--DELIMETER-FOR-PARSER--")
    for sql_statement in sql_statements:
        cursor.execute(sql_statement)

    connection.commit()
    print(f"{file} runned successfully")
    cursor.close()


if __name__ == "__main__":
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )

    run_sql(connection, "./src/db/schema.sql")
    run_sql(connection, "./src/db/data.sql")
