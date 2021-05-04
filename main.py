import mysql_handle
import get_professors_comments

if __name__ == '__main__':

    index = 0
    offset = 0
    page_size = 100
    professors_count = mysql_handle.select_count('professors')


    while index <= professors_count:
        professors = mysql_handle.select_professors_by_paging(page_size, offset)

        for professor in professors:
            professor_list = list(professor)
            get_professors_comments.get_professors_comment_by_node_id(professor_list[1])
            index = index + 1
            print(index, professor_list[1])

        offset = offset + page_size
