from flask import Flask, request, url_for, render_template
import json

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

	return crime_id