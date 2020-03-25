# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
import time



def scrape_all():
    news  = scrape_news()
    return {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image' : link,
        'weather': weather_tweet,    
        'facts': mars_df,
        'last_modified': hemi_img_urls
    }

def scrape_news():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    # URL of page to be scraped
    url ='https://mars.nasa.gov/news'
    browser.visit(url)
    html = browser.html

    # Retrieve page with the requests module
    response = requests.get(url)

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Extract article title and paragraph text
    slide= soup.select_one('ul.item_list li.slide')
    #article = slide.find("div", class_='list_text')
    news_title = slide.find("div", class_="content_title").text.strip()
    news_p = slide.find("div", class_ ="article_teaser_body").text

    return {
        'title': news_title,
        'paragraph': news_p
    }

def scrape_images():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit url for JPL Featured Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    feat_image=browser.find_by_id('full_image').click()
    browser.is_element_present_by_text('more info', wait_time=2)

    browser.click_link_by_partial_text('more info')
    html2 = browser.html

    # Retrieve page with the requests module
    response = requests.get(image_url)

    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html2, "html.parser")
    #print(image_soup)

    # Scrape the URL
    featured_image= image_soup.find('figure', class_= 'lede').a['href']
    link = f'https://www.jpl.nasa.gov{featured_image}'
    print(link)
    
    return {
        'Image Link': link
    }


def scrape_weather():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    Twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(Twitter_url)
    html3 = browser.html
    time.sleep(5)

    # Parse HTML with Beautiful Soup
    Twt_soup = BeautifulSoup(html3, 'html.parser')

    # Extract latest tweet
    weather_tweet= Twt_soup.findAll("span", class_= "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    weather_tweet()

    return {
        'Weather Forecast': weather_tweet
    }

def scrape_facts():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'
    html_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame and assign columns
    mars_df = html_facts[0]
    mars_df.columns = ['Description','Value']

    # Save html code 
    mars_df.to_html()

    mars_df

    return {
        'mars facts': mars_df
    }

def hemisphere():

    # Visit the USGS Astrogeology Science Center Site
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemi_img_urls = []

    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append List
        hemi_img_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
        

    hemi_img_urls

    return {
        'Hemisphere Image URLS': hemi_img_urls
    }