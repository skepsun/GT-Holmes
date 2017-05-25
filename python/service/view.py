import json
from flask import Flask, request, url_for, render_template

# from engine.

app = Flask(__name__)

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/searchCrimeId", methods=["POST", "GET"])
def searchCrimeId():
	if request.method == "POST":
		para_dict = json.loads(request.data)
		crime_id   = para_dict["crimeId"]
		threshold  = para_dict["threshold"]
		start_time = para_dict["startTime"]
		end_time   = para_dict["endTime"]

	print crime_id

	result = {
		"status": 0,
		"res": [
			{ "position": { "lat": 33.7490, "lng": -84.3880 }, "similarity": 0.5 }
		]
	}

	return json.dumps(result)