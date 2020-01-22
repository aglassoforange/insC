import requests
import re
import urllib.request
import json
import time as tt
import random
import threading
import progressbar
import queue
import Filewriting


class Crawlposts():

    def __init__(self):
        self.default_frontpage_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                      ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                      ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0'
        }


        self.default_json_frontpage_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                      ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                      ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0'
        }


    def checker(self,number_post,current_post):
        if(current_post<number_post):
            pass
        else:
            self.whether_next_post = False


    def requests_frontpage(self,url_queue,detialpage_queue,save_queue,number_post):
        basic_info = []
        while True:
            args=url_queue.get()
            print(args)
            output_list=[]
            if len(args)== 1:
                url = "https://www.instagram.com/" + args[0] + "/"
                headers = self.default_frontpage_headers
                try:
                    response = requests.get(url, headers=headers)
                    tt.sleep(100)
                    file = response.text
                except Exception as e:
                    print(e)
                html = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>',
                                 file).group(1)
                html_json = json.loads(html)
                try:
                    user = html_json['entry_data']['ProfilePage'][0]['graphql']['user']
                    edge_owner = user['edge_owner_to_timeline_media']
                    edges = edge_owner['edges']
                    page_infor=edge_owner['page_info']
                    list_2=[]
                    id = user['id']
                    username = html_json['entry_data']['ProfilePage'][0]['graphql']['user']['username']
                    post_count=edge_owner['count']
                    test_count = 0
                    basic_info.append(id)
                    basic_info.append(username)
                    basic_info.append(post_count)
                    save_queue.put(basic_info)
                    has_next_page=page_infor['has_next_page']
                    list_2.append(id)
                    list_2.append(page_infor['end_cursor'])
                    url_queue.put(list_2)
                    for edge in edges:
                        test_count += 1
                        node =edge['node']
                        id_pic = node['id']
                        display_url = node['shortcode']
                        comment_count = node['edge_media_to_comment']['count']
                        time = node['taken_at_timestamp']
                        data = {}
                        out_json = data
                        out_json['id_pic'] = id_pic
                        out_json['display_url'] = display_url
                        out_json['comment_count'] = comment_count
                        out_json['time'] = time
                        output_list.append(out_json)
                        detialpage_queue.put(display_url)
                    print(has_next_page == False)
                    if (has_next_page == False):
                        print('processing ending')
                        url_queue.task_done()
                        break

                except Exception as e:
                    print(e)

            if len(args)==2:
                tittle = 'https://www.instagram.com/graphql/query/'
                headers = self.default_json_frontpage_headers

                try:
                    default_vars = {
                        "query_hash": "e769aa130647d2354c40ea6a439bfc08",
                        "id": args[0], "first": "12", "after":args[1]
                    }
                    response_j = requests.get(tittle, headers=headers, params=default_vars)
                    tt.sleep(random.random() * 100)
                    response_j=response_j.text
                except Exception as e:
                    print(e)

                response_j = str(response_j)
                result = json.loads(response_j)
                try:
                    edge_owner_j= result['data']['user']['edge_owner_to_timeline_media']
                    count_j = edge_owner_j['count']
                    page_infor_j=edge_owner_j['page_info']
                    has_next_page_j = page_infor_j['has_next_page']
                    cursor_j = page_infor_j['end_cursor']
                    list_2 = []
                    list_2.append(basic_info[0])
                    list_2.append(cursor_j)
                    url_queue.put(list_2)
                    print(cursor_j)
                    edges_j = edge_owner_j['edges']
                    test_count = 0
                    for edge_j in edges_j:
                           # if (number_post <= basic_info[2] ):
                                test_count += 1
                                id_pic_j = edge_j['node']['id']
                                display_url_j = edge_j['node']['shortcode']
                                comment_count_j = edge_j['node']['edge_media_to_comment']['count']
                                time_j = edge_j['node']['taken_at_timestamp']
                                data_j = {}
                                out_json_j = data_j
                                out_json_j['id_pic'] = id_pic_j
                                out_json_j['display_url'] = display_url_j
                                detialpage_queue.put(display_url_j)
                                out_json_j['comment_count'] = comment_count_j
                                out_json_j['time'] = time_j
                                output_list.append(out_json_j)
                    save_queue.put(output_list)
                    print(cursor_j==None)
                    if cursor_j== None:
                        url_queue.task_done()
                        break

                except Exception as e:
                    print(e)



        url_queue.task_done()

    def a(self,queue):
        while True:
            print(queue.get())
            queue.task_done()

    def b(self, queue):
        while True:
            print(queue.get())
            queue.task_done()




