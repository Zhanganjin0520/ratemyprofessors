import mysql.connector

mydb = mysql.connector.connect(
    host="139.196.164.139",
    port="3306",
    user="root",
    password="rootpwd",
    database="rate_professors"
)
cursor = mydb.cursor()


def insert_professors(professors_arrays):
    sql = "INSERT INTO professors (node_id, tid, firstname, lastname, department, school_id, school_name, rates, avg_rate, avg_difficulty)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, professors_arrays)
    mydb.commit()
    print(cursor.rowcount, "was inserted.")


def select_professors_by_paging(page_size, page_num):
    cursor.execute("SELECT * FROM professors ORDER BY id LIMIT %s OFFSET %s " % (page_size, page_num))
    return cursor.fetchall()


def select_professors_by_node_id_paging(professors_node_id, page_size, page_num):
    vars = (professors_node_id, page_size, page_num)

    cursor.execute(
        "SELECT * FROM professors WHERE node_id = %s ORDER BY id LIMIT %s OFFSET %s ", vars)
    return cursor.fetchall()


def select_count(table_name):
    cursor.execute("SELECT count(*) FROM %s" % (table_name))
    return cursor.fetchall()[0][0]


def insert_professors_comments(professors_comment_arrays):
    sql = "INSERT INTO professors_comment (professor_node_id,rate_node_id,class,clarity_rating,helpful_rating,difficulty_rating,comment,date)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, professors_comment_arrays)
    mydb.commit()
    print(cursor.rowcount, "was inserted.")
