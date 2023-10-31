import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openai

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
}

openai.api_key = os.environ["OPENAI_API_KEY"]

class Scrap:
    def __init__(self, meta_data, search_tags):
        self.meta_data = meta_data
        self.search_tags = search_tags

    def gen_content(self, tag_class, tag_list):
        # if self.meta_data['source'] == 'url':
        #     htmlLink = self.meta_data['url']
        #     r = requests.get(htmlLink, headers=headers)
        #     soup = BeautifulSoup(r.content, "html.parser")
        # else:
        soup = BeautifulSoup(self.meta_data['content'], "html.parser")
        content = []
        for item in tag_list:
            item_list = soup.find_all(tag_class, {"class": item})
            list_len = len(item_list)
            for i in range(list_len):
                content_temp = item_list[i].get_text().strip()
                if content_temp != '':
                    content.append(content_temp)
        return content

    def gen_content_dict(self, search_dict):
        
        content_dict = {}
        for key in search_dict.keys():
            content_dict[key] = self.gen_content(key, search_dict[key])
        return content_dict

    def gen_content_list(self, content):
        content_list = []
        for key in content.keys():
            content_list += content[key]
        return content_list

    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, 
        )
        return response.choices[0].message["content"]

    def gen_tag(self, content_list):
        tag_list = []
        for item in content_list:
            prompt = f"""
            Your task is to generate an one-sentence searchable tagline or question for the given content within 20 words. \
            You should use plain language, and don't mention the terms like 'the context' or 'content: ',\
            the output should be a string of text without unnecessary quotation marks.\
            The content is: ```{item }```
            """
            response = self.get_completion(prompt)
            tag_list.append(response)
        return tag_list
    
    def gen_df(self):
        content_dict = self.gen_content_dict(self.search_tags)
        content_list = self.gen_content_list(content_dict)
        tag_list = self.gen_tag(content_list)
        df = pd.DataFrame({'tag': tag_list, 'content': content_list})
        for key in self.meta_data.keys():
            if key != 'content':
                df[key] = self.meta_data[key]
        # df['content'] = content_list
        return df
    
class manualAdd:
    def __init__(self, tag_list, content_list, meta_data):
        self.tag_list = tag_list
        self.content_list = content_list
        self.meta_data = meta_data

    def gen_df(self):
        df = pd.DataFrame({'tag': self.tag_list, 'content': self.content_list})
        for key in self.meta_data.keys():
            if key != 'content':
                df[key] = self.meta_data[key]
        return df