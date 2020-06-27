from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import whois
from geotext import GeoText
import yaml
import urllib.request
from inscriptis import get_text

document = open('config.yaml', 'r')
parsed = yaml.load(document, Loader=yaml.FullLoader)


class Ext:

    id = ''
    phone = []
    email = []
    name = ''
    postcode = []
    foundedon = []
    parent = ''
    city = []
    country = {}

    def __init__(self, url):
        self.url = url
        self.code = ''
        self.CompanyType = ''
        self.name = ''
        self.owner = ''
        self.revenue = ''
        self.address = ''

    def findlinks(self):

        Ext.id = self.url
        hyperlinks = []
        crawl = []


        try:
            html = urlopen(self.url)

        except:
            if "http" in self.url:
                self.url = "https" + self.url.strip("http")
                html = urlopen(self.url)
            else:
                print("not good url try again!")
                return

        soup = BeautifulSoup(html, features="lxml")
        try:
            w = whois.whois(self.url)
        except:
            print("who is failed")

        dn = w["domain_name"]
        pa = w["registrar"]

        Ext.name = dn[0].split('.')[0]
        Ext.parent = pa

        if w.Keys is not None:
            Ext.email = (w["emails"])
    
        check = self.url.split('.')
        count = 0

        for ch in check:
            if re.search(parsed['domains'], ch, re.IGNORECASE):
                count += 1
            else:
                start = ch
        
        all_links = soup.find_all("a")
        
        for link in all_links:
            hyperlinks.append(link.get("href"))
            if link.get("src") is not None:
                hyperlinks.append(link.get("src"))
                
        if count == len(check):
            if Ext.name == '':
                Ext.name = self.url
            start = "uk"
        else:
            Ext.name = start

        for ele in hyperlinks:
            if ele is not None and type(ele) == str:
                if re.search(parsed['crawler'], ele, re.IGNORECASE):
                    if (ele is not None and start in ele) or (ele is not None and ele.startswith(self.url)):
                        if ele not in crawl:
                            if "lenses" not in ele:
                                if "https://" in ele or "http://" in ele:
                                    crawl.append(ele)
        if "www" in self.url:
            Ext.name = self.url.split('.')[1]
        else:
            Ext.name = self.url.split('.')[0].strip("http:/").strip("https:/")
        return crawl        
        
    def extract(self):
        
        try:
            html = urllib.request.urlopen(self.url).read().decode('utf-8')
        except:
            print("not good url try again!")
            return

        sitetext = get_text(html)

        for listingdates in parsed['regex']['-dates']:
            dates = re.findall(listingdates, sitetext)
        for listingpostal in parsed['regex']['-postal']:
            postal = re.findall(listingpostal, sitetext)
        for listingemail in parsed['regex']['-email']:
            email = re.findall(listingemail, sitetext)
        for listingphone in parsed['regex']['-phone']:
            phone = re.findall(listingphone, sitetext)

        places = GeoText(sitetext)
        Ext.city = places.cities
        Ext.country = GeoText(sitetext).country_mentions

        for post in postal:
            if post not in Ext.postcode:
                Ext.postcode.append(post)
                
        for num in phone:
            if num not in Ext.phone:
                Ext.phone.append(num)
        
        for mailid in email:
            if mailid not in Ext.email:
                Ext.email.append(mailid.strip('0123546789-'))
                
        for date in dates:
            if date not in Ext.foundedon:
                Ext.foundedon.append(date)

    def printing(self):

        retdict = {}
        retdict['url'] = Ext.id
        retdict["name"] = Ext.name
        retdict["parent"] = Ext.parent

        numberlist = [None] * 1
        indexer = 0
        for ele in Ext.phone:
            for st in ele:
                if st == " ":
                    ele = ele.remove(" ")
                else:
                    if re.search(".*\\d+.*", st):
                        if indexer == 0:
                            numberlist[indexer] = st
                            indexer += 1
                        else:
                            numberlist.append(st)

        if "null" in numberlist:
            numberlist.remove(None)
        if " " in numberlist:
            numberlist.remove(" ")
        if "" in numberlist:
            numberlist.remove("")

        retdict["phone"] = list(dict.fromkeys(numberlist))
        retdict["email"] = list(dict.fromkeys(Ext.email))
        retdict["postcode"] = list(dict.fromkeys(Ext.postcode))
        retdict["foundedon"] = list(dict.fromkeys(Ext.foundedon))
        retdict["city"] = list(dict.fromkeys(Ext.city))
        retdict["country"] = list(dict.fromkeys(Ext.country))
        return retdict
      
#to rebug the code uncomment the following lines and start
#url = input("enter the url:")
#obj = ext(url)
#urllist = obj.findlinks()

#if urllist is None:
#    sys.exit()
#urllist.append(url)
#print(urllist)

#my_objects = []

#for i, craw in enumerate(urllist):
    
#    my_objects.append(ext(craw))
#    my_objects[i].extract()

#obj.printing()
    
    



