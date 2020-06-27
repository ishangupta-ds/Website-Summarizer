API for web crawling,dataextraction and keyword extraction for a website(company) and NLP Engine for review analysis.

Version:1.0

Features:
Email search,
Url search.

results:
website url,
phone,
email,
name,
postcode,
foundedon,
parent,
city,
country.

usage instructions:
follow instructions.txt,
start the server/API running api.py file,
serach/call using endpoints.

Endpoints:
localhost:5000/urlsearch?id=<url>,
localhost:5000/emailsearch?id=<mailid for http sites preferable>.

config:
add to regex in config.yaml to improve search,
add to crawler in config.yaml to improve search urls for crawler,
add to domains in config.yaml to improve search on domains,
add to stopwords.txt for refined search.

future dev checklist:
proxy service,
https sites using email,
customer review anaysis,
clients for the company,
comparision of APIs,
improve regex,
create database for previous searches,
generalize for all countries,
search for company type,code,address,owner,
post request instead of get.
