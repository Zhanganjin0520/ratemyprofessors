import lxml.html
import requests
import scrapy
import json
import mysql_handle


def get_professor_cursor(first_name):
    url = "https://www.ratemyprofessors.com/search/teachers"
    r = requests.get(url, params={'query': first_name})
    root = lxml.html.fromstring(r.content)
    selector = scrapy.Selector(text=r.text, type="html")
    s = selector.xpath("//script[contains(., 'window.__RELAY_STORE__')]/text()").re_first(
        'window.__RELAY_STORE__ = (.*);')

    json_obj = json.loads(s)

    # to get count and cursor
    result_count_key = 'resultCount'
    result_cursor_key = 'cursor'
    result_count = 0
    result_cursor = ''
    for key in json_obj:
        if result_count == 0:
            try:
                result_count = json_obj[key][result_count_key]
            except:
                print('------- no total count -----------')

        if result_cursor == '':
            try:
                result_cursor = json_obj[key][result_cursor_key]
                print(result_cursor)
            except:
                print('--------- no cursor ------------------------')

    return (result_count, result_cursor)


def get_professors(first_name):
    (result_count, result_cursor) = get_professor_cursor(first_name)
    # post teacher data
    teacher_data_url = 'https://www.ratemyprofessors.com/graphql'
    # teacher query json request
    teacher_data_request = {
        "query": "query TeacherSearchPaginationQuery(\n  $count: Int!\n  $cursor: String\n  $query: TeacherSearchQuery!\n) {\n  search: newSearch {\n    ...TeacherSearchPagination_search_1jWD3d\n  }\n}\n\nfragment TeacherSearchPagination_search_1jWD3d on newSearch {\n  teachers(query: $query, first: $count, after: $cursor) {\n    edges {\n      cursor\n      node {\n        ...TeacherCard_teacher\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n    resultCount\n  }\n}\n\nfragment TeacherCard_teacher on Teacher {\n  id\n  legacyId\n  avgRating\n  numRatings\n  ...CardFeedback_teacher\n  ...CardSchool_teacher\n  ...CardName_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment CardFeedback_teacher on Teacher {\n  wouldTakeAgainPercent\n  avgDifficulty\n}\n\nfragment CardSchool_teacher on Teacher {\n  department\n  school {\n    name\n    id\n  }\n}\n\nfragment CardName_teacher on Teacher {\n  firstName\n  lastName\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n",
        "variables": {"count": 0, "cursor": "",
                      "query": {"text": "", "schoolID": ""}}}
    teacher_data_request['variables']['count'] = result_count
    teacher_data_request['variables']['cursor'] = result_cursor
    teacher_data_request['variables']['query']['text'] = first_name
    # teacher query request headers
    headers = {'Authorization': 'Basic dGVzdDp0ZXN0'}
    # post request
    teacher_data_res = requests.post(teacher_data_url, json=teacher_data_request, headers=headers, timeout=20)
    professors_arrays = []
    if teacher_data_res.status_code == 200:
        # to handle response data
        teacher_data = json.loads(teacher_data_res.text)
        teacher_edges = teacher_data['data']['search']['teachers']['edges']
        for edge in teacher_edges:
            teacher_node = edge['node']
            teacher_node_id = teacher_node['id']
            teacher_id = teacher_node['legacyId']
            firstname = teacher_node['firstName']
            lastname = teacher_node['lastName']
            rates = teacher_node['numRatings']
            department = teacher_node['department']
            school_id = teacher_node['school']['id']
            school_name = teacher_node['school']['name']
            avg_rates = teacher_node['avgRating']
            avg_difficulty = teacher_node['avgDifficulty']

            professor_base = [teacher_node_id, teacher_id, firstname, lastname, department, school_id, school_name,
                              rates, avg_rates, avg_difficulty]
            professors_arrays.append(professor_base)

            if len(professors_arrays) >= 500:
                # save to mysql db
                mysql_handle.insert_professors(professors_arrays)
                professors_arrays = []

    # save to mysql db
    mysql_handle.insert_professors(professors_arrays)
