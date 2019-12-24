#coding=utf-8
#这是一个抓取解析ins 个人主页的程序

import requests
import re
import urllib.request
import json
import time as tt
import random


class Crawl_ins():

    outputlist = []
    has_next_page = True
    cursor=""
    comment_cusor=""
    comment_output = []
    has_next_comment_page = True

    #得到个人首页
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
        try:
            response = requests.get(url, headers=headers)
            tt.sleep(random.random())
            return response.text
        except Exception as e:
             print(e)

    #解析HTML界面
    def html_parse_key(self, file):
        html = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>', file).group(1)
        html_json=json.loads(html)
        try:
            edges=html_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
            self.has_next_page=html_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            self.cursor=html_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            id = html_json['entry_data']['ProfilePage'][0]['graphql']['user']['id']
            username = html_json['entry_data']['ProfilePage'][0]['graphql']['user']['username']
            test_count = 0
            for edge in edges:
                test_count+=1
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
            return id, username, self.has_next_page, self.cursor ,self.outputlist,test_count
        except Exception as e:
            print(e)

    #解析json
    def json_parse_key(self, file ):
        file = str(file)
        result = json.loads(file)
        try:
            count=result['data']['user']['edge_owner_to_timeline_media']['count']
            self.has_next_page=result['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            self.cursor=result['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            edges = result['data']['user']['edge_owner_to_timeline_media']['edges']
            test_count = 0
            for edge in edges:
                test_count+=1
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
            return self.outputlist, count, self.has_next_page, self.cursor,test_count
        except Exception as e:
            print(e)

    #去下一个json
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
            try:
                response = requests.get(tittle, headers=headers, params=vars)
                tt.sleep(random.random())
                return response
            except Exception as e:
                print(e)

    #在有下一页的情况下
    def automation_next(self, name):
        cp = Crawl_ins()
        html =cp.get_id(name)
        answer= cp.html_parse_key(html)
        id = answer[0]
        count = answer[5]
        try:
            while cp.has_next_page is True:
                json=cp.get_next_pagejson(cp.cursor, id)
                json=json.text
                count1=cp.json_parse_key(json)[4]
                count +=count1
            return cp.outputlist,count
        except Exception as e:
            print(e)

    #得到一页的评论，输出表格
    def get_page(self,display_url):
        title = 'https://www.instagram.com/p/'+display_url+'/'
        url = '\'/p/'+display_url+'/\''
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                      ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                      ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'cache-control': 'max-age=0'
        }
        try:
            html = requests.get(title, headers=headers)
            tt.sleep(random.random())
        except Exception as e:
            print(e)
        html = html.text
        html=str(html)

        try:
            midwork = re.search(r'<script type="text/javascript">window.__additionalDataLoaded((.*?));</script>', html).group(2)
            start = midwork.find(',')
            end = midwork.find(');</script>')
            output = (midwork[start+1:end])
            html_json=json.loads(output)
            shortcode = html_json['graphql']['shortcode_media']['shortcode']
            self.comment_cusor = html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
            self.has_next_comment_page = html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
            edges = html_json['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
            test_count = 0
            newlist =[]
            newlist.append(display_url)
            for edge in edges:
                data = {}
                test_count= test_count+1
                commenter_id = edge['node']['owner']['id']
                commenter_name = edge['node']['owner']['username']
                comment = edge['node']['text']
                time = edge['node']['created_at']
                profile_pic = edge['node']['owner']['profile_pic_url']
                comment_liked  = edge['node']['edge_liked_by']['count']
                commenter_page = 'https://www.instagram.com/'+commenter_name+'/'
                out_json = data
                out_json['time'] = time
                out_json['id'] = commenter_id
                out_json['name'] = commenter_name
                out_json['text'] = comment
                out_json['commenter\'pic'] = profile_pic
                out_json['comment like quantity'] = comment_liked
                out_json['commenter\'s profile page'] = commenter_page
                newlist.append(out_json)
            self.comment_output.append(newlist)
            return test_count
        except Exception as e:
            print(e)
    #解析每一页的json 输出表格
    def get_page_json(self,url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'ig_did=B6A0EBE8-3CC7-4A42-AD88-56EEBC3FE1A7; mid=Xe9AHwALAAFnS3pWPfUiZd7mU3G5; fbm_124024574287414=base_domain=.instagram.com;'
                      ' csrftoken=OJnzccnHaQyEjSUpgZGfFoQVCXUG2wq3; shbid=12239; shbts=1575960619.8887541; ds_user_id=2164068030;'
                      ' sessionid=2164068030%3AD8dWOTnFw5PhZ7%3A2; rur=ASH; urlgen="{\"103.95.207.86\": 136600}:1ifIYs:Hf0dUoHWtu4_9ctmx0cP8Fr1TRk"',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'cache-control': 'max-age=0'
        }
        vars = {
            "query_hash": "97b41c52301f77ce508f55e66d17620e",
            "shortcode": url, "first": "12", "after": str(self.comment_cusor)
        }
        url = 'https://www.instagram.com/graphql/query/'
        try:
            file = requests.get(url, headers=headers, params=vars)
            tt.sleep(random.random())
        except Exception as e:
            print(e)
        file = file.text
        analysis = json.loads(str(file))
        try:
            self.has_next_comment_page = analysis['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
            self.comment_cusor = analysis['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
            edges = analysis['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
            test_count = 0
            for edge in edges:
                data = {}
                test_count = test_count+1
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

    #根据页面名称 打开页面，收集留言
    def automation_in_page(self, display_url):
        dp = Crawl_ins()
        count = dp.get_page(display_url)
        print(count)


        try:
            while dp.has_next_comment_page:
                count=count+dp.get_page_json(display_url)
            return dp.comment_output, count
        except Exception as e:
            print(e)

if __name__=="__main__":
    start = tt.time()
    ic = Crawl_ins()
    output,count=ic.automation_next('_lhyaaaaan')
    print(count)
    page_link=[]
    print(output)
    for op in output :
        page_link.append(op['display_url'])
        print(page_link)
    for link in page_link:
        ic.automation_in_page(link)
    print(ic.comment_output)
    print(ic.outputlist)
    end =tt.time()

    print('operating time is %d seconds long'%(end-start))
