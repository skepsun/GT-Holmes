import json
from flask import Flask, request, url_for, render_template

from dao import DBConnecter
from holmes.features.bow.feature import Feature

app = Flask(__name__)

f = Feature()

url   = "https://139.162.173.91:3000/api/basic_infos"
token = "gatech1234!"

basic_infos = DBConnecter(url, token)

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/searchCrimeId", methods=["POST", "GET"])
def searchCrimeId():
	crime_id   = ""
	limit      = 1
	start_time = 0
	end_time   = 0

	if request.method == "POST":
		para_dict = json.loads(request.data)
		crime_id   = para_dict["crimeId"]
		limit      = int(para_dict["limit"])
		start_time = para_dict["startTime"]
		end_time   = para_dict["endTime"]

	matched_crimes = f.query_via_id(crime_id, limit)

	disp_crimes = []
	for id, sim, pos, desc in matched_crimes:
		if id != "0":
			print id, sim, pos, desc
			real_pos = [float(basic_infos["id"]["avg_lat"])/100000, float(basic_infos["id"]["avg_long"])/100000]
			disp_crimes.append([id, sim, real_pos, desc])

	if matched_crimes == None:
		return json.dumps({
			"status": 1,
			"msg": "Invalid Crime ID"
		})
	else:
		return json.dumps({
			"status": 0,
			"res": [ { 
				"position": { "lat": pos[0], "lng": pos[1] }, 
				"similarity": float(sim), 
				"id": id, 
				"label": desc } 
				for id, sim, pos, desc in matched_crimes ]
		})

	