#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:45:21 2019

@author: joe
"""
from nytimesarticle import articleAPI
from bs4 import BeautifulSoup
import time, requests

dev_key = "dGbfLeJfxGPaMNH6uVDhuZo7JBdCNLJB"
api = articleAPI(dev_key)

out_stream = open("output.txt", "w+")

def get_article(url_):
    r = requests.get(url_)
    if r.status_code != 200:
        return -1
    
    outstring = ""
    
    soup = BeautifulSoup(r.content, "html.parser")
    pgraphs = soup.find_all('p') 
    for p in pgraphs:
        outstring += p.get_text()
    
    return outstring    

def worker(begin, end, npages=100):
    articles = api.search(begin_date=begin, end_date=end)
    time.sleep(6)
    hits = articles['response']['meta']['hits']
    pages = int(hits/10)
    pages = pages if pages <=100 else 100 
    
    for page in range(1, pages+1):
        print("Page: ", str(page), "/", str(pages))
        b_time = time.time()
        articles = api.search(begin_date=begin, end_date=end, page=page)
        num_arts = len(articles['response']['docs'])
        
        for art in range(0, num_arts):
            url = articles['response']['docs'][art]['web_url']
            text = get_article(url)
            if text != -1:
                out_stream.write(text)
        if (time.time() - b_time) < 6:
            time.sleep(6 - (time.time()-b_time))

worker(20131231, 20141231)    
    