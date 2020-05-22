# # import json

# # json_file = open("data.json",'r')
# # v = json.loads(json_file.readline())
# # print(v[0])
# # v.append({"name":"jas"})
# # print(v)
# # json_file.close()
# # json_file  = open("data.json",'w')
# # json_file.write(json.dumps(v))
# from datetime import datetime
# now = datetime.now()
# print(str(now))


path = '/post'
print(path.strip('/'))