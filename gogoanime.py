import requests
from bs4 import BeautifulSoup
import os

searchurl='https://www.gogoanime.tv/search.html?keyword='
searchq = input('search: ')
page = requests.get(searchurl+searchq)

pagedata=page.text

def websoup(webpagedata):   
    soup=BeautifulSoup(webpagedata,'html.parser')
    resultuls=soup.find_all('p',attrs={'class':'name'})
    
    results=[]
    for resultul in resultuls:
        namechild=resultul.find('a')
        results.append(namechild)

    titles=[]
    links=[]
    
    for result in results:
        titles.append(result['title'])
        links.append('https://gogoanime.tv'+result['href'])

    title_link_dictionary=dict(zip(titles, links))

    return title_link_dictionary

def numberofpages(webpagedata):  
    try:
        soup=BeautifulSoup(webpagedata,'html.parser')
        pagination=soup.find('ul',attrs={'class':'pagination-list'})
        lis=pagination.find_all('li')
        return len(lis)
    except:
        return None

titlelinks=websoup(pagedata)
for titlelink in titlelinks.keys():
    print(titlelink)

print()

if numberofpages(pagedata)==None:
    pagetitlelinks=titlelinks
#    series = input('choose series: ')
#    print(titlelinks[series])

else:
    pagepos=1
    pagetitlelinks = titlelinks

    while True:
       
        print('|Previous-page||Next-page|')
        print()
        
        pageno=input('if your series is on this page enter this: ')
        
        if pageno == 'next':
            pagepos=pagepos+1
            r=requests.get(searchurl+searchq+'&page='+str(pagepos))
            pagetitlelinks=websoup(r.text)
            
            for pagetitlelink in pagetitlelinks.keys():
                print(pagetitlelink)
            print()
            
        elif pageno == "prev":
            pagepos=pagepos-1
            r=requests.get(searchurl+searchq+'&page='+str(pagepos))
            pagetitlelinks=websoup(r.text)
            
            for pagetitlelink in pagetitlelinks.keys():
                print(pagetitlelink)
            print()
            
        elif pageno == "this":
            break
        
        else:
            print('unexpected input please trry again')
    
    
series = int(input('choose series: '))
#print(pagetitlelinks[series])
#print(list(pagetitlelinks.values())[series-1])

episodenumber=input('enter eepisode number: ')

#link to the series fetched using number instead of full name
serieslink=list(pagetitlelinks.values())[series-1]
#fetching the name of the series in the format which is used in url so that it can be used in fetching the url of the episode
animename=serieslink.split('/')[len(serieslink.split('/'))-1]

## getting the link to the episode of the series selected and parsing its html

episoderequest=requests.get('https://gogoanime.tv/'+animename+'-episode-'+str(episodenumber))
tempsoup=BeautifulSoup(episoderequest.text,'html.parser')

# fetching link to vidstream where download link to direct video is.

downloadanime=tempsoup.find('div',attrs={'class':'download-anime'})
downloadlinkpagea=downloadanime.find('a')
downloadlinkpage=downloadlinkpagea['href']

# fetching the direct link

directrequest=requests.get(downloadlinkpage)
directsoup=BeautifulSoup(directrequest.text,'html.parser')
directdivs=directsoup.find('div',attrs={'class':'dowload'})
directlinka=directdivs.find('a')
directlink=(directlinka['href'])

print(directlink)




        
