import requests, json, io, pandas, os
import html_parser


# reading query.csv file onto a pandas csv object
query_colnames = ["tags","is_answered","view_count","answer_count","score","last_activity_date","creation_date","last_edit_date","question_id","content_license","link","title","body","code"]
#				   tags;  is_answered;  view_count;  answer_count;  score;  last_activity_date;  creation_date;  last_edit_date;  question_id;  content_license;  link;  title;  body;  code
extracted_questions = "python_queries.csv"
run_data = pandas.read_csv(extracted_questions,header=0,names=query_colnames)

# extracting the question_ids column onto a list
question_ids=run_data.question_id.tolist()


for id in question_ids:
	print("Extracting the answers for query "+ str(id))
	query_answers = "query_answers" + str(id) +".json"
	request_statement = "https://api.stackexchange.com/2.3/questions/" +str(id) +"/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody"
	r = requests.get(request_statement)
	scraped_data = json.loads(r.text)

	data_json = open(query_answers, "w")
	json.dump(scraped_data,data_json)
	data_json.close()

# reading from JSON file and writinc onto a CSV file
goal_file = "python_answers.csv"
fp = io.open(goal_file,"a", encoding = "utf-8")
fp.write('"is_accepted","score","last_activity_date","creation_date","answer_id","question_id","body","code"\n') # 


for id in question_ids:

	answer_file = "query_answers" + str(id) +".json"
	f_out = io.open(answer_file, encoding = "utf-8")
	answers = json.loads(f_out.read())

	item = answers["items"]
	for i in range(len(item)):
		if "is_accepted" in item[i]:
			is_accepted = str(item[i]["is_accepted"])
		else:
			is_accepted = ""
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
		if "answer_id" in item[i]:
			answer_id = str(item[i]["answer_id"])
		else:
			answer_id = ""
		if "question_id" in item[i]:
			question_id = str(item[i]["question_id"])
		else:
			question_id = ""
		if "body" in item[i]:
			text = str(item[i]["body"])
			body = html_parser.parse_body(text)
			code = html_parser.parse_code(text)
		else:
			body = ""
			code = ""
		fp.write( '"' + is_accepted + '","' + score + '","' + last_activity_date  + '","' + creation_date + '","' + answer_id + '","' + question_id  + '","' + body  + '","' + code + '"\n') #  

fp.close()
