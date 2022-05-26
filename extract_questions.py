import requests, json, io, pandas, os
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import html_parser

page_size = 100  # number of queries to be extracted in each call
page_num = 1    # number of the page that will be extracted
api_key = "*zJ7yWEg0FQGbAIUV17t2Q(("

json_dir = os.getcwd() + "/json_questions"
if not os.path.exists(json_dir):
    os.mkdir(json_dir)

print("Extracting Python Queries")
"""
for page_num in range(100,150):
        python_queries_json = json_dir + "/python_queries"+ str(page_num) +".json"
        f = open(python_queries_json, "w")

        # requesting query data from stack exchange
        request_statement = "https://api.stackexchange.com/2.3/tags/python/faq?page=" + str(page_num) + "&pagesize=" + str(page_size) + "&site=stackoverflow&key="+api_key+"&filter=withbody"
        r = requests.get(request_statement)

        print("Page: "+ str(page_num) )
        scraped_data = (json.loads(r.text))

        # checking if the scraper has reach the quota of scraping limit
        quota = scraped_data["quota_remaining"]
        json.dump(scraped_data, f)

        f.close()
"""

# Writing extracted data on a csv file
print("Converting to .csv format" )

goal_file = "python_queries.csv"
fp = io.open(goal_file,"a", encoding = "utf-8")
fp.write(' "tags","is_answered","view_count","answer_count","score","last_activity_date","creation_date","last_edit_date","question_id","content_license","link","title","body","code"\n') # 

for page_num in range(100,143):

        python_queries_json =json_dir + "/python_queries"+ str(page_num) +".json"
        f_out = io.open(python_queries_json, encoding = "utf-8")
        queries = json.loads(f_out.read())
        
        item = queries["items"]
        for i in range(len(item)):
                if "tags" in item[i]:
                        tags = str(item[i]["tags"]).replace(',',';')
                else:
                        tags = ""
                if "is_answered" in item[i]:
                        is_answered = str(item[i]["is_answered"])
                else:
                        is_answered = ""
                if "view_count" in item[i]:
                        view_count = str(item[i]["view_count"])
                else:
                        view_count = ""
                if "answer_count" in item[i]:
                        answer_count = str(item[i]["answer_count"])
                else:
                        answer_count = ""
                if "score" in item[i]:
                        score = str(item[i]["score"])
                else:
                        score = ""
                if "last_activity_date" in item[i]:
                        last_activity_date = str(item[i]["last_activity_date"])
                else:
                        last_activity_date = ""
                if "creation_date" in item[i]:
                        creation_date = str(item[i]["creation_date"])
                else:
                        creation_date = ""
                if "last_edit_date" in item[i]:
                        last_edit_date = str(item[i]["last_edit_date"])
                else:
                        last_edit_date = ""
                if "question_id" in item[i]:
                        question_id = str(item[i]["question_id"])
                else:
                        question_id = ""
                if "content_license" in item[i]:
                        content_license = str(item[i]["content_license"])
                else:
                        content_license = ""
                if "link" in item[i]:
                        link = str(item[i]["link"])
                else:
                        link = ""
                if "title" in item[i]:
                        text = str(item[i]["title"])
                        title = html_parser.parse_body(text)
                else:
                        title = ""
                if "body" in item[i]:
                        text = str(item[i]["body"])
                        body = html_parser.parse_body(text)
                        code = html_parser.parse_code(text)
                else:
                        body = ""
                        code = ""
                fp.write( '"' + tags + '","' + is_answered + '","' + view_count + '","' + answer_count + '","' + score + '","' + last_activity_date  + '","' + creation_date + '","' + last_edit_date + '","' + question_id + '","' + content_license + '","' + link + '","' + title + '","' + body  + '","' + code +'"\n') #  
                # 
fp.close()


