#parse all the links on search result page of talking.com

import requests
from bs4 import BeautifulSoup
import time

domain_url = "http://www.intalking.com/"
serp_url = 'http://www.intalking.com/search.php?mod=forum&searchid=17&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=%E8%B3%87%E7%94%9F%E5%A0%82'


#find all the page links (in h3 tag) 
def serp_title_link():
    h3 = soup.find_all("h3")
    for link in h3:
        a = link.a.get("href")
        whole_a = domain_url + a
        url_list.append(whole_a)


#next page 
def next_page_link():
    if soup.find('div',class_='pg').find("a", class_="nxt") != None:
        #there is no 'next page' in the last page
        next_page = soup.find('div',class_='pg').find("a", class_="nxt").get("href")
        next_page_url = domain_url + next_page
        #print(next_page_url)
        return(next_page_url)
        

url_list = []
sleep = 0.1    
    

while True:
    page = requests.get(serp_url).text
    soup = BeautifulSoup(page, 'html.parser')
    serp_title_link()
    next_page_link()
    #break when the last page is finished
    if next_page_link() == None:
        break
    serp_url = next_page_link()
    time.sleep(sleep)
    sleep += 0.01
    
    
print(len(url_list))


def page_text(forum_url):
    url_inside = forum_url
    inside_text = requests.get(url_inside).text
    inside_soup = BeautifulSoup(inside_text, "html.parser")

    #all tds in this page
    all_td = inside_soup.find_all('td',class_='t_f')

    #td[0] ,split it 
    if inside_soup.find('td',class_='t_f') != None:
        all_td1 = inside_soup.find('td',class_='t_f').text
        all_td1_split = all_td1.split("\n")

        length = len(all_td)  #length of all_td
        text_list = []  #list for text in this page


        #deal with td[0]
        unwanted = ['馬上加入美妝IN TALKING 可以看到更多美資訊喔', 
                    '您需要 登錄 才可以下載或查看，沒有帳號？註冊 ', 
                    '下載附件',
                    'x',
                    '\r']
        all_td1_split = list(filter(lambda x : x not in unwanted, all_td1_split))

        for word in all_td1_split:
            if ".jpg" not in word and "保存到相冊" and "天前 上傳" not in word:
                text_list.append(word)


        #deal with td[1:] 
        for i in range(1, len(all_td)):
            comment_i = all_td[i].text
            comment_i_split = comment_i.split("\n")
            for c in comment_i_split:
                text_list.append(c)


        #strip the text in text_list
        new_text_list = []  
        for text in text_list:
            a = text.strip()
            if len(a) != 0:
                if "\xa0" in a:
                    b = a.replace("\xa0", "")
                    new_text_list.append(b)
                else:
                    new_text_list.append(a)


        return(new_text_list)
    
    
    else:
        return(" ")
        
        
        
       

text_dict = {}


sleep2 = 0.1

for url in url_list:
    text_dict[url] = page_text(url)
    time.sleep(sleep2)
    sleep2 += 0.01       
