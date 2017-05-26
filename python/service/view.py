import json
from flask import Flask, request, url_for, render_template

from engine.features.selfbuilt.feature import Feature

app = Flask(__name__)

f = Feature()



@app.route("/map")
def map():
    return render_template("map.html")



@app.route("/searchCrimeId", methods=["POST", "GET"])
def searchCrimeId():
	if request.method == "POST":
		para_dict = json.loads(request.data)
		crime_id   = para_dict["crimeId"]
		limit      = para_dict["limit"]
		start_time = para_dict["startTime"]
		end_time   = para_dict["endTime"]

	result = {
		"status": 0,
		"res": [ { "position": { "lat": pos[0], "lng": pos[1] }, "similarity": sim } 
			for id, sim, pos, desc in f.query_via_id(crime_id, limit) ]
	}

	return json.dumps(result)