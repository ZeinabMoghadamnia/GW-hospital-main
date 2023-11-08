import psycopg2
from configparser import ConfigParser


def config(filename=None, section=None):
    parser = ConfigParser()
    parser.read(filename)

    db_config = dict()
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]

    else:
        raise Exception(f'section {section}')

    return db_config


def connect(conn, cur):
    if conn and cur:
        conn, cur, local_connection = conn, cur, False
    else:
        try:
            params = config('database.ini', 'xxxx')
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            local_connection = True


        except (Exception, psycopg2.DatabaseError) as e:
            print(e, e.__traceback__.tb_lineno)
            print(__file__)

            conn, cur, local_connection = None, None, None

    return conn, cur, local_connection


# connect(None, None)
