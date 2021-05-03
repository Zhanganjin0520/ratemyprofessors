import mysql_handle
import get_professors_comments

if __name__ == '__main__':
    professors = mysql_handle.select_professors_by_node_id_paging('VGVhY2hlci0xNDg0MTc3', 10, 0)
    professors_count = mysql_handle.select_count('professors')

    index = 517
    offset = 0
    page_size = 10
    while index <= professors_count:
        professors = mysql_handle.select_professors_by_paging(page_size, offset)
        offset = offset + 10

        for professor in professors:
            professor_list = list(professor)
            get_professors_comments.get_professors_comment_by_node_id(professor_list[1])
            index = index + 1
            print(index)

    if index > professors_count:
        professors = mysql_handle.select_professors_by_paging(page_size, professors_count)
        for professor in professors:
            professor_list = list(professor)
            get_professors_comments.get_professors_comment_by_node_id(professor_list[1])
