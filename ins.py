#coding=utf-8
import requests
import re
import urllib.request
import json

class Crawl_ins():
    outputlist = []
    has_next_page = True
    cursor=""
    comment_cusor=""
    count=0
    comment_output = []

    def crawl_ins(url):
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
        reponse = requests.get(url, headers=headers)
        data = reponse.text
        json_data = json.loads(data)

    def get_id(self, name):
        url = "https://www.instagram.com/"+name+"/"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                      ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                      ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0'
        }

        response = requests.get(url, headers=headers)
        return response.text

    def html_parse_key(self, file):
        html = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>', file).group(1)
        html_json=json.loads(html)
        edges=html_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        self.has_next_page=html_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        self.cursor=html_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        id = html_json['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        username = html_json['entry_data']['ProfilePage'][0]['graphql']['user']['username']
        for edge in edges:
            self.count+=1
            id_pic = edge['node']['id']
            display_url = edge['node']['shortcode']
            comment_count = edge['node']['edge_media_to_comment']['count']
            time = edge['node']['taken_at_timestamp']
            data = {}
            out_json = data
            out_json['id_pic'] = id_pic
            out_json['display_url'] = display_url
            out_json['comment_count'] = comment_count
            out_json['time'] = time
            self.outputlist.append(out_json)
        return id, username, self.has_next_page, self.cursor ,self.outputlist


    def json_parse_key(self, file ):
        file = str(file)
        result = json.loads(file)
        if 'errors' not in result:
            count=result['data']['user']['edge_owner_to_timeline_media']['count']
            self.has_next_page=result['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            self.cursor=result['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            edges = result['data']['user']['edge_owner_to_timeline_media']['edges']
            for edge in edges:
                self.count += 1
                id_pic=edge['node']['id']
                display_url = edge['node']['shortcode']
                comment_count = edge['node']['edge_media_to_comment']['count']
                time = edge['node']['taken_at_timestamp']
                data = {}
                out_json = data
                out_json['id_pic'] = id_pic
                out_json['display_url'] = display_url
                out_json['comment_count'] = comment_count
                out_json['time'] = time
                self.outputlist.append(out_json)
            return self.outputlist, count, self.has_next_page, self.cursor

    def get_next_pagejson(self, end_cursor , id):
            tittle= 'https://www.instagram.com/graphql/query/'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                          ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                          ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0'
            }

            vars={
                "query_hash": "e769aa130647d2354c40ea6a439bfc08",
                "id": str(id), "first": "12", "after": str(self.cursor)
            }
            response = requests.get(tittle, headers=headers, params=vars)
            return response

    def automation_next(self, name):
        cp = Crawl_ins()
        html =cp.get_id(name)
        id = cp.html_parse_key(html)[0]
        while cp.has_next_page is True:
            json=cp.get_next_pagejson(cp.cursor, id)
            json=json.text
            cp.json_parse_key(json)
        print(cp.count)
        return cp.outputlist

    def get_page(self,display_url):
        title = 'https://www.instagram.com/p/'+display_url+'/'
        url = '\'/p/'+display_url+'/\''
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                      ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                      ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
            #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            #'accept-encoding': 'gzip, deflate, br',
            #'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            #'cache-control': 'max-age=0'
        }
        html = requests.get(title, headers=headers)
        html = html.text
        html=str(html)
        midwork =re.search(r'<script type="text/javascript">window.__additionalDataLoaded((.*?));</script>', html).group(2)
        start = midwork.find(',')
        end = midwork.find(');</script>')
        output = (midwork[start+1:end])
        html_json=json.loads(output)
        shortcode = html_json['graphql']['shortcode_media']['shortcode']
        self.comment_cusor = html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']

        self.has_next_page = html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
        edges = html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']

        for edge in edges:
            comment = edge['node']['text']
            time = edge['node']['created_at']
            profile_pic = edge['node']['owner']['profile_pic_url']
            comment_liked  = edge['node']['edge_liked_by']['count']
            print(comment)
        return comment
if __name__=="__main__":
    dp = Crawl_ins()
    output1 = dp.get_page('B55lfabgXYF')
    print(output1)
