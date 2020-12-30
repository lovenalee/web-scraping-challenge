#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
    

def scrape_info():

    browser = init_browser()

    mars_dict = {}
        
    url='https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')


    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='rollover_description_inner').text
    news_p = soup.find('div', class_='article_teaser_body').text



    # ## JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image at https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # Assign the url string to a variable called featured_image_url.
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html_image = browser.html
    soup = bs(html_image, "html.parser") 


    # Make sure to find the image url to the full size .jpg image.
    image_url = soup.find("a", class_ = "button fancybox")["data-fancybox-href"]

    # Make sure to save a complete url string for this image.
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + image_url
 

    # ## Mars Facts
    # Visit the Mars Facts webpageand use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # https://space-facts.com/mars/
    url3 = 'https://space-facts.com/mars'
    browser.visit(url3)
    tables = pd.read_html(url3)
    table_df = tables[0]
    table_df.columns = ['Facts', 'Value']
    table_df['Facts'] = table_df['Facts'].str.replace(':', '')

    # Use Pandas to convert the data to a HTML table string.
    table_html = table_df.to_html()
   

    mars_dict['table_html']=table_html
    # ## Mars Hemispheres
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres. 
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(url4)
    html_images = browser.html
    soup = bs(html_images, "html.parser") 
    print(soup.prettify())


    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    items = soup.find_all('div', class_='item')
 
    # Save both the image url string for the full resolution hemisphere image, 
    # and the Hemisphere title containing the hemisphere name. 
    titles = []
    urls = []
    for item in items:
        titles.append(item.find('h3').text.strip())
        urls.append(base_url + item.find('a')['href'])

    image_urls = []
    for url in urls:
        browser.visit(url)
        html_images = browser.html
        soup = bs(html_images, "html.parser") 
        image_url = soup.find("img", class_ = "wide-image")["src"]
        image_urls.append(base_url+image_url)




    # Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.
    image_dic = []

    for i in range(len(titles)):
        image_dic.append({'title':titles[i],'img_url':image_urls[i]})


    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(table_html),
        "hemisphere_images": image_dic
    }
    

    browser.quit()
    return mars_dict




