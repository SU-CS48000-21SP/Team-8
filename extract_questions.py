import requests, json, io, pandas, os


python_queries = "Desktop/CS 58005/stackoverflow_python_queries.json"
"""
params = {
    "key": "tDLQTdhmdB97",
    "type": jsontext
}
"""
# request_statement = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&tagged=python&site=stackoverflow"
request_statement = "https://api.stackexchange.com/2.3/tags/python/faq?site=stackoverflow"

r = requests.get(request_statement)

print("Extracting Python Queries")
scraped_data = (json.loads(r.text))
data_json = open(python_queries, "w")
json.dump(scraped_data, data_json)
data_json.close()


#csvData = data_json.to_csv(index=False)
