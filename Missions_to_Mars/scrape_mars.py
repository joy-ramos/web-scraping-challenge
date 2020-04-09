#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import cssutils
import requests
import time

def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--enable-javascript")
    return Browser('chrome', **executable_path, headless=True, options=chrome_options)


# In[2]:
def scrape_info():

    browser = init_browser()

    #Final dictionary to be returned by this function
    mars_data = {}

    

    #NASA Mars News
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(2)

    soup = BeautifulSoup(browser.html, 'html.parser')

    news_article = soup.find('ul', class_='item_list').find('li', class_='slide')

    #news_article

    #News title and article teaser
    news_title = news_article.find('div', class_='content_title').text
    news_p = news_article.find('div', class_='article_teaser_body').text
    
    mars_data.update({'news_title': news_title, 'news_body': news_p})

    # news_title
    # news_p

    #JPL Mars Space Images - Featured Image
    
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    
    time.sleep(1)

    soup = BeautifulSoup(browser.html, 'html.parser')

    featured = soup.find('section', class_='primary_media_feature')
    featured_article_style = featured.find('div', class_= 'carousel_items').article['style']
    style = cssutils.parseStyle(featured_article_style)
    
    url = style['background-image']
    url = url.replace('url(', '').replace(')', '')
    complete_url = 'https://www.jpl.nasa.gov' + url

    mars_data.update({'featured_image': complete_url})
    complete_url


    #Mars Weather
    
    r = requests.get('https://twitter.com/marswxreport?lang=en')
    soup = BeautifulSoup(r.text, 'html.parser')

    tweet = soup.find('div', class_='js-tweet-text-container')

    for a in tweet.findAll('a'):
        a.decompose()

    tweet_p = tweet.p.text    
    mars_weather = tweet_p.replace('\n', ',').replace('\r', ',')
    
    mars_data.update({'mars_weather': mars_weather})
    mars_weather
    

    #Mars Facts (Table)

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    
    df = tables[2]
    df = df.rename(columns={0: "Desription", 1: "Value"})
    df = df.to_html(index=False)
    
    mars_data.update({'mars_facts': df})


    #Mars Hemispheres

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    soup = BeautifulSoup(browser.html, 'html.parser')

    div = soup.find('div', class_='collapsible results')
    div = div.findAll('div', class_='item')

    hemisphere_image_urls = []

    for item in div:
        link = item.find('a', class_='itemLink product-item')
        img = link.find('img', class_='thumb')
        description = item.find('div', class_='description')
        
    #    print(link['href'])
    #    print(item.prettify())
        title = description.a.text
        print(description.a.text)
        
        url2 = 'https://astrogeology.usgs.gov'+link['href']
    #    print(url2)
        browser.visit(url2)
        soup = BeautifulSoup(browser.html, 'html.parser')
        
        img = soup.find('img', class_='wide-image')
        img_url = 'https://astrogeology.usgs.gov' + img['src']
        print(img['src'])
        
        print("\n")
        
        hemisphere_image_urls.append({'title': title,'img_url':img_url})
        
    mars_data.update({'hemisphere_images': hemisphere_image_urls})

    browser.quit()
    
    print ("Final Dictionary")
    print ("\n")
    print (mars_data)
    return (mars_data)
