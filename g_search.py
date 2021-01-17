
'''
The MIT License (MIT)
Copyright (c) 2014 Patrick Olsen
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

First Author: Michael Spencer Email: mwspencer75@gmail.com
Second Author :Mohammad Hossein sharifi Email : mh.sh7676@gmail.com

version :1.0.1
'''

#Starting Messing with this Version, Version 9 is the robust one

#googe_search
#Uses Beautiful soup and webdriver to google search an imported url
#Then returns the related url from html
#Then searches that url, and so on and so forth.

#Using lxml parser

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unicodecsv as csv
from urllib import parse
import time
# url = 'https://www.google.com/search?q=What+are+the+best+tools+for+finding+Instagram+influencers&rlz=1C1CHFX_enUS601US601&oq=What+are+the+best+tools+for+finding+Instagram+influencers&aqs=chrome..69i57.24849j0j7&sourceid=chrome&ie=UTF-8'
url = 'https://www.google.com/search?q=%D9%81%D8%B1%D9%88%D8%B4+%DA%86%D8%B1%D8%AE+%D8%AE%DB%8C%D8%A7%D8%B7%DB%8C&oq=%D9%81%D8%B1%D9%88%D8%B4+%DA%86%D8%B1%D8%AE+%D8%AE%DB%8C%D8%A7&aqs=chrome.0.0i19l2j69i57j0i19l5.6343j0j7&sourceid=chrome&ie=UTF-8'

rel_link_search_dir = "Related_Results.txt" #enter path to new text file here
rec_search_dir = "Recommended_Results.txt"
rel_parse_dir = "Related_Parsed.txt"
rec_parse_dir = "Recommended_Parsed.txt"
# search_val = "How to get more instagram followers"
search_val = "فروش چرخ خیاطی"

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

def get_related_search(url):
    """Creates a list of href from the class _e4d"""
    rel_links = [] 
    driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options) 
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    links = soup.select("p.nVcaUb a[href]") 
    raw_related_search = soup.select("p.nVcaUb a span") 

    for link in links: 
        rel_link = link['href']
        rel_links.append(str(rel_link))
    related_search = [rel.get_text() for rel in raw_related_search]
    driver.close()
    return rel_links ,related_search
    
def get_recommended_search(url, search_val):
    """Creates a list of recommended searches"""
    reco_words = []
    driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options) 
    driver.get("http:\\www.google.com")
    search = driver.find_element_by_name('q')
    search.send_keys(search_val)
    time.sleep(8)
    soup = BeautifulSoup(driver.page_source, "lxml")
    recommendations = soup.select("div.sbl1 span")
    
    for reco in recommendations:
        reco_word = reco
        # reco_words.append(search_val + reco_word.get_text())
        reco_words.append(reco_word.get_text())
    driver.close()
    return reco_words
    
        
    
    
def write_to_file(dir, results):
    """writes file to directory"""
    for res in results:
        with open(dir, "a") as f:
            f.write(str(res) + "\n") 
        f.close()


def read_on_file(dir) :
    """read file to directory"""
    with open(dir, "r") as f:
        content = f.readlines()
        f.close()
    return content

def parse_data(fname, dir):
    """Parses the google searches, then creates a list of the words"""
    lists_words = list()
    data = list()
    try:
        fhand = open(fname)
    except:
        print("This is not a file name")
        quit()
    for line in fhand:
        line = line.split("=")
        line = line[2].split("&sa")
        line = line[0].split("+")
        lists_words.append(line)
    for lists in lists_words:
        for word in lists:
            data.append(word)
    return data
    
def get_count(results):
    """Creates a dictionary, word being the key, and word count being the value"""
    counts_dict = dict()
    for word in results:
        counts_dict[word] = counts_dict.get(word, 0) + 1
    return counts_dict
    
def create_csv(counts_dict):
    """Creates a csv of the dictionary"""
    with open('key_words.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Word', 'Count'])
        for key, value in counts_dict.items():
            writer.writerow([key, value])
    csv_file.close()
    
# def main(url, rel_link_search_dir, rec_search_dir, rel_parse_dir, search_val, numTime):
def main(rel_link_search_dir="Related_Results.txt", rec_search_dir="Recommended_Results.txt",rel_word_search_dir="related_search.txt",\
    rel_parse_dir="Related_Parsed.txt", search_val="a28", numTime=1):
    #url: url to search
    #rel_link_search_dir: directory to save related search text file
    #rec_search_dir: directory to save recommeded text file 
    #numTime: number of times to search
    i = numTime
    j = numTime
  
    print("Working on recommendation")
    for x in range(j):
        
        reco_words = get_recommended_search('http://www.google.com', search_val)
        write_to_file(rec_search_dir, reco_words)
        # for rec in reco_words :
        #     # print("{:::::::::::::::::",rec)
        #     new_reco_words = get_recommended_search('http://www.google.com', rec)
        #     write_to_file(rec_search_dir, new_reco_words)

    print("Working on related searches")
    lines = read_on_file(rec_search_dir)
    
    for line in lines:
        url = "https://www.google.com/search?safe=active&sxsrf=ALeKk01d-O0nbkFoi9zNeShPD3b9Iw2Uow%3A1610656302142&ei=LqoAYNCXCJC-a763gvgM&q={}&gs_ssp=eJzj4tTP1TcwyzCptDRg9BK4ue_Gxhubb-672XGz5XbPjc0AsmgPEA&oq=%D9%BE%D8%B1&gs_lcp=CgZwc3ktYWIQAxgBMgQIIxAnMgUILhDJAzICCAAyAggAMgIILjICCC4yAgguMgIIADICCAAyAggAOgQIABBHOgUIABDJAzoICC4QxwEQrwE6BwgAEMkDEB46BAgAEB5Q7ipYu0Vg81FoAnAEeACAAbICiAH_CJIBBTItMy4xmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab".\
            format(parse.quote(line))
        # url = "https://www.google.com/search?q={}".format(parse.quote(search_val))
        rel_links,related_search = get_related_search(url)
        print("rel link : ",rel_links)
        write_to_file(rel_link_search_dir, rel_links)
        print(type(related_search))
        print(type(related_search)=='bs4.element.ResultSet')
        write_to_file(rel_word_search_dir, related_search)
        # for rel in rel_links : 
        #     print(rel)
        #     print(type(rel))
        #     # url = 'https://www.google.com' + rel
        #     # print('url',url)
        
        
    # print("Working on parsing data to text.")
    # data_rel = parse_data(rel_link_search_dir, rel_parse_dir)
    # #data_rec = 
    # print("Working on dictionary")
    # dict_count = get_count(data_rel)
    # print("These are the counts: ", dict_count)
    # print("Now creating csv of counts")
    # create_csv(dict_count)
    # print("All done!  Check out the results in whichever folder you ran this script.")        
    return rec_search_dir,rel_word_search_dir
# main(url, rel_link_search_dir, rec_search_dir, rel_parse_dir, search_val, 1)
# main(rel_link_search_dir, rec_search_dir, rel_parse_dir, search_val, 1)

main(search_val="وحید شکری")







