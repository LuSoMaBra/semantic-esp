import psycopg2
from configparser import ConfigParser

def read_config(filename='scrapies-esp/settings.ini', section='server_postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def connectDB():
    conn = None
    try:
        params = read_config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn

def testDB():
    conn = connectDB()
    try:
        cur = conn.cursor()
        print('Database connection opened.')

        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print('PostgreSQL database version:' + str(db_version))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn


def selectDB(connection, string_sql):
    if not connection:
        connection = connectDB()
    try:
        cursor = connection.cursor()
        cursor.execute(string_sql)
        count = cursor.rowcount
        print("Result ", cursor.fetchall())
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting record", error)
    finally:
        if cursor:
            cursor.close()


def insertDB(connection, tabela, fields, values):

    fields_sql = " ("
    for x in fields:
        fields_sql = fields_sql + str(x) + ", "
    fields_sql = fields_sql[:-2] + ") "

    values_sql = " values ("
    for x in values:
        values_sql = values_sql + "'" + str(x) + "', "
    values_sql = values_sql[:-2] + ") "

    string_sql = "insert into " + tabela + fields_sql + values_sql

    print(string_sql)

    try:
        cursor = connection.cursor()
        cursor.execute(string_sql)
        connection.commit()
        print("Record inserted successfully ({})".format(cursor.rowcount))
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting record", error)
    finally:
        if cursor:
            cursor.close()


if __name__ == '__main__':
    conn = testDB()
    if conn is not None:
        conn.close()
        print('Database connection closed.')
