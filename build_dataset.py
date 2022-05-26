import requests, json, io, pandas


query_colnames = ["tags","is_answered","view_count","answer_count","score","last_activity_date","creation_date","last_edit_date","question_id","content_license","link","title","body","code"]
queries = pandas.read_csv("python_queries.csv",header=0,names=query_colnames)

answer_colnames = ["is_accepted","score","last_activity_date","creation_date","answer_id","question_id","body","code"]
answers = pandas.read_csv("python_answers.csv",header=0,names=answer_colnames)

merged_data = queries.merge(answers,on=["question_id"],how='left',suffixes=("","left"))
merged_data.to_csv("complete.csv")

max = merged_data.groupby("scoreleft").max()
max.head()