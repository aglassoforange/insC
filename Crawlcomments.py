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


class Crawlcomments():

    def __init__(self):
                self.default_json_frontpage_headers ={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                    'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                              ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                              ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'cache-control': 'max-age=0'
                }

                self.default_frontpage_headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                    'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                              ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                              ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'cache-control': 'max-age=0'
                }

    def crawlcomments(self, detail_queue, save_queue):
        newlist = []
        while True:
            display_url = detail_queue.get()
            if len(display_url)==1:
                    title = 'https://www.instagram.com/p/' + display_url + '/'
                    try:
                        html = requests.get(title, headers=self.default_frontpage_headers)
                        tt.sleep(random.random()*100)
                    except Exception as e:
                        print(e)
                    html = html.text
                    html=str(html)
                    try:
                        midwork = re.search(
                            r'<script type="text/javascript">window.__additionalDataLoaded((.*?));</script>', html).group(2)
                        start = midwork.find(',')
                        end = midwork.find(');</script>')
                        output = (midwork[start + 1:end])
                        html_json = json.loads(output)
                        shortcode = html_json['graphql']['shortcode_media']['shortcode']
                        page_info=html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']
                        comment_cusor = page_info['end_cursor']
                        list_1 = []
                        list_1.append(shortcode)
                        list_1.append(comment_cusor)
                        detail_queue.put(list_1)
                        has_next_comment_page = \
                        page_info['has_next_page']
                        edges = html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
                        test_count = 0
                        newlist.append(display_url)
                        for edge in edges:
                            data = {}
                            test_count = test_count + 1
                            commenter_id = edge['node']['owner']['id']
                            commenter_name = edge['node']['owner']['username']
                            comment = edge['node']['text']
                            time = edge['node']['created_at']
                            profile_pic = edge['node']['owner']['profile_pic_url']
                            comment_liked = edge['node']['edge_liked_by']['count']
                            commenter_page = 'https://www.instagram.com/' + commenter_name + '/'
                            out_json = data
                            out_json['time'] = time
                            out_json['id'] = commenter_id
                            out_json['name'] = commenter_name
                            out_json['text'] = comment
                            out_json['commenter\'pic'] = profile_pic
                            out_json['comment like quantity'] = comment_liked
                            out_json['commenter\'s profile page'] = commenter_page
                            newlist.append(out_json)


                        if(has_next_comment_page==False):
                            detail_queue.task_done()
                            break

                    except Exception as e:
                        print(e)


            if(len(display_url) ==2):
                vars = {
                    "query_hash": "97b41c52301f77ce508f55e66d17620e",
                    "shortcode": display_url[0], "first": "12", "after": str(display_url[1])
                }
                url = 'https://www.instagram.com/graphql/query/'
                try:
                    file = requests.get(url, headers=self.default_json_frontpage_headers, params=vars)
                    tt.sleep(100)



                    file = file.text
                    analysis = json.loads(str(file))
                    try:
                        self.has_next_comment_page = \
                        analysis['data']['shortcode_media']['edge_media_to_parent_comment']['page_info'][
                            'has_next_page']
                        self.comment_cusor = \
                        analysis['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
                        edges = analysis['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
                        test_count = 0
                        for edge in edges:
                            data = {}
                            test_count = test_count + 1
                            commenter_id = edge['node']['owner']['id']
                            commenter_name = edge['node']['owner']['username']
                            comment = edge['node']['text']
                            time = edge['node']['created_at']
                            profile_pic = edge['node']['owner']['profile_pic_url']
                            comment_liked = edge['node']['edge_liked_by']['count']
                            commenter_page = 'https://www.instagram.com/' + commenter_name + '/'
                            out_json = data
                            out_json['time'] = time
                            out_json['id'] = commenter_id
                            out_json['name'] = commenter_name
                            out_json['text'] = comment
                            out_json['commenter\'pic'] = profile_pic
                            out_json['comment like quantity'] = comment_liked
                            out_json['commenter\'s profile page'] = commenter_page
                            self.comment_output.append(out_json)
                        return test_count
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)