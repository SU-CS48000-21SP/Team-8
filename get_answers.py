import requests, json, io, pandas, os

log_colnames = ["tags","is_answered","view_count","answer_count","score","last_activity_date","creation_date","last_edit_date","question_id","content_license","link","title"]
extracted_questions = "Desktop/CS 58005/stackoverflow_python_queries.csv"
run_data = pandas.read_csv(extracted_questions,header=0,names=log_colnames)
question_ids=run_data.question_id.tolist()

query_answers = "Desktop/CS 58005/query_answers.json"
for id in question_ids:

    """
    params = {
      "api_key": "tDLQTdhmdB97",
      "run_token":token,
      "format": "json"
    }
    """
    
    request_statement = "https://api.stackexchange.com/2.3/questions/" +str(id) +"/answers?order=desc&sort=activity&site=stackoverflow"
    r = requests.get(request_statement)
    scraped_data = json.loads(r.text)

    data_json = open(query_answers, "w")
    json.dump(scraped_data,data_json)
    data_json.close()

