import json, io, pandas

# Run Info File

print("Converting to .csv format:" + '\n')

source_file = "Desktop/CS 58005/stackoverflow_python_queries.json"
f = io.open(source_file, encoding = "utf-8")

data = json.loads(f.read())
goal_file = "Desktop/CS 58005/stackoverflow_python_queries.csv"
item = data["items"]

fp = io.open(goal_file,"w", encoding = "utf-8")
# 
fp.write(' "tags","is_answered","view_count","answer_count","score","last_activity_date","creation_date","last_edit_date","question_id","content_license","link","title"\n')
for i in range(len(item)):
        
        if "tags" in item[i]:
                tags = str(item[i]["tags"]).replace(',',';')
        else:
                tags = ""
        """
        if "owner" in item[i]:
                owner = str(item[i]["owner"]).replace(',',';')
        else:
                owner = ""
        """
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
                title = str(item[i]["title"])
        else:
                title = ""
        fp.write( '"' + tags + '","' + is_answered + '","' + view_count + '","' + answer_count + '","' + score + '","' + last_activity_date  + '","' + creation_date + '","' + last_edit_date + '","' + question_id + '","' + content_license + '","' + link + '","' + title + '"\n')
        # 
f.close()
fp.close()

