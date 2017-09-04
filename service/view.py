#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the main script for a Flask project, which defines various of interfaces for getting 
access to backend services or data. 
"""
import time 
import json
from flask import Flask, request, url_for, render_template

from dao import BasicInfo, ReportText
#from holmes.features.bow.feature import Feature

app = Flask(__name__)

# Global Variables
token = "gatech1234!"

# Data Handler
basic_info_handler  = BasicInfo(token)
report_text_handler = ReportText(token)

# NLP Model
#f = Feature()

# Renderring main web page
@app.route("/map")
def Map():
    return render_template("map.html")

# API for searching correlated crime records via crime id
@app.route("/searchCrimeId", methods=["POST"])
def searchCrimeId():
	crime_id   = ""
	limit      = 1
	start_time = 0
	end_time   = 0


	# Parse requested parameters
	if request.method == "POST":
		para_dict  = json.loads(request.data)
		crime_id   = para_dict["crimeId"]
		limit      = int(para_dict["limit"])
		start_time = int(para_dict["startTime"]/1000) # change milliseconds to seconds by /1000
		end_time   = int(para_dict["endTime"]/1000)   # change milliseconds to seconds by /1000
	else:
		return json.dumps({
			"status": 1,
			"msg": "Invalid Request Type"})

	if start_time < 0: # no input at start time   
		start_time = 0
	if end_time < 0: # no input at end time 
		end_time = int(time.time())

	print "start timestamp: ",start_time, "end timestamp: ", end_time

	# Get matched crime records by input crime id
	# matched_crimes = f.query_via_id(crime_id)
	# matched_crimes = f.query_via_id(crime_id,limit)
	# if matched_crimes == None:
	# 	return json.dumps({
	# 		"status": 1,
	# 		"msg": "Invalid Crime ID"})
	# print "matched_crimes", matched_crimes
	matched_crimes = [['163560154', 0.20330104, 'ROB-STREET-GUN'], ['153322796', 0.2092959, 'ROB-STREET-GUN'], ['162021796', 0.21052736, ''], ['161070352', 0.21449465, 'ROB-STREET-GUN'], ['150772900', 0.23019572, ''], ['163572101', 0.30466831, 'FRAUD-IMPERS.<$10,000'], ['160362333', 0.40189749, 'THEFT OF TRUCK/VAN/BUS'], ['153142632', 0.41234228, 'DAMAGE TO PROP PRIVATE'], ['170160001', 1.0000001, 'Ped Robbery'], ['170152497', 1.0000001, 'ROB-STREET-GUN']]

	# Transpose the 2D list "matched_crimes". 
	# And get informations by fields
	trans_mat    = map(list, zip(*matched_crimes)) # For Python 3.x: list(map(list, zip(*matched_crimes)))
	ids          = trans_mat[0]
	sims         = trans_mat[1]
	descs        = trans_mat[2]
	# Retrieve matched crime records' related informations by their ids.
	# Including: GPS positions, updated dates, and so on
	basic_infos  = basic_info_handler.get("incident_num", ids)
	
	print "Type of basic_infos: ", type(basic_infos)
	# set time limit
	for i in range(len(basic_infos)-1,-1,-1):
		if basic_infos[i]["date"] < start_time or basic_infos[i]["date"] > end_time:
			basic_infos.pop(i)
			ids.pop(i)
			sims.pop(i)
			descs.pop(i)

	basic_infos = basic_infos[-limit:]
	ids         = ids[-limit:]
	sims        = sims[-limit:]
	descs       = descs[-limit:]


	#dates        = [ basic_info["date"] for basic_info in basic_infos ]
	dates 		 = [basic_info["incident_date_timestamp"] for basic_info in basic_infos ]
	print "dates", dates,ids
	cities       = [ basic_info["city"] for basic_info in basic_infos ]
	positions    = [ (basic_info["avg_lat"], basic_info["avg_long"]) for basic_info in basic_infos ]
	priorities   = [ basic_info["priority"] for basic_info in basic_infos ]

	categories   = [ basic_info["category"] for basic_info in basic_infos ]
	incident_date_timestamp = [basic_info["incident_date_timestamp"] for basic_info in basic_infos ]
	# print "incident_date_timestamp: ",incident_date_timestamp
	if len(ids) > 0 :
		report_texts = report_text_handler.get("incident_num", ids)
		update_dates = [ report_text["update_date"] for report_text in report_texts ]
		remarks      = [ report_text["remarks"] for report_text in report_texts ]
	else:
		print "No items return"

	# Return reorganized data to the front-end
	return json.dumps({
		"status": 0,
		"res": [{
			"id": ids[ind], 
			"similarity": float(sims[ind]), 
			"label": categories[ind],
			"position": { "lat": positions[ind][0], "lng": -1 * positions[ind][1] },
			"city": cities[ind],
			"priority": priorities[ind],
			"update_dates": update_dates[ind],
			"date": dates[ind],

			"incident_date_timestamp": incident_date_timestamp[ind],

			"text": remarks[ind] }
			for ind in range(len(ids))
			if len(ids[ind]) >= 9 ]})



# API for searching correlated crime records by keywords
@app.route("/searchKeywords", methods=["POST"])
def searchKeywords():
	keywords   = ""
	limit      = 1
	start_time = 0
	end_time   = 0
	# Parse requested parameters
	if request.method == "POST":
		para_dict  = json.loads(request.data)
		keywords   = para_dict["keywords"].strip()
		limit      = int(para_dict["limit"])
		start_time = int(para_dict["startTime"])
		end_time   = int(para_dict["endTime"])
	else:
		return json.dumps({
			"status": 1,
			"msg": "Invalid Request Type"})

	matched_items = report_text_handler.getMatchedKeywords(keywords, limit)
	#matched_items = [{'remarks': u'On 01-01-2012 at around 0010Hrs, I Ofc. S.Green was dispatched to a Vandalism call at 2841 browns Mill Rd. I arrived on scene at 0020Hrs. Upon my arrival I met with the Victim Ms. Niterrius Ann Sanders. Ms. Sanders advised during the time of 0000Hrs She heard multiple gun shots go off next door, where 9 of them pierce threw her the side of her house. She advised her daughter Marquisha Sanders and her cousin Queen Burdette were also in the house but, nobody was hurt or injured. Ms. Sanders had bullet holes on the right side of her house which penetrated into the one of the bed rooms wall and ceiling along with the living room wall and ceiling. Ms. Sanders advised soon as I pulled up in the drive way the group of perpetrator left the location where the shooting where coming from. Ms. sanders did advise she did not see who was shooting but she heard it . She advises she knows its her next door neighbor. She advised all night before the shooting they where drinking and smoking.During my investigation Zone 3 Sgt... Ryan radio#1393 was raised about this incident. G.I. Investigator Buckles radio #4383 was advised of this incident. Do to the new year along with the massive amount of calls the city were receiving. I was advised by Inv... Buckles not to raise I.D. because know body was hurt and their was no suspect that could be identified as the shooter. 19 shell casing was retrieved between 2841 Browns Mill and 2843.  One bullet was found on the floor of Ms. Sanders living room. All items was put into property as evidence. Ms Sanders received a copy of the incident case report. The investigation continues.', 'update_date': 1357280059, 'id': u'130010022'}, {'remarks': u'On January 1st, 2013 I (Ofc. C.S. Thornton) conducted the arrest of an intoxicated driver at 19 Joseph E. Lowery Blvd NW. I was positioned at 3 Joseph E. Lowery Blvd SW observing traffic within the area. Next, I observed a vehicle (2000 - Chevrolet / Tahoe: GA# AGX2060) traverse northbound on Joseph E. Lowery Blvd SW/NW across Martin Luther King Jr. Dr. through a solid red light. The vehicle traversed beyond the threshold of the protected north and southbound turning signals active on Martin Luther King Jr. Dr.The vehicle was stopped at the above incident location to investigate further. Making contact with the driver (Mr. Ricardo Sheats) I immediately smelled the heavy scent of alcoholic beverage upon his breath. Advising Mr. Sheats of his infraction, I could clearly see Mr. Sheats\'s eyes were glassy, but not blood shot. Also, I could see in plain view a can which appeared to be a malt alcoholic beverage in the middle console. Asking Mr. Sheats for his drivers identification card, he advised he didn\'t have it in his possession.Due to the high New Year vehicle / pedestrian traffic and sporadic celebratory gun fire Mr. Sheats was taken to my vehicle for safety and cover. As I escorted Mr. Sheats to my vehicle, the can was identified as an opened 12oz Budweiser malt beverage. Mr. Sheats was advised he was being detained in order to investigate the infraction further. It was evident Mr. Sheats was under the influence of alcohol as he walked unsteady, as well as his clothing was disheveled.Since the initial contact, Mr. Sheats was highly apologetic, repeatedly advising he didn\'t do anything wrong. I asked Mr. Sheats from the back of the vehicle would he mind asking some basic questions in order to determine his sobriety. First, I asked Mr. Sheats how much alcohol did he consume prior to operating the vehicle. Mr. Sheats advised he had 1 to 2 beers, which was last consumed (3) three hours ago. Next, he was asked when was the last time he ate, Mr. Sheats replied he last ate at 1:00PM on December 31, 2012. Finally, he was asked where he was coming from, Mr. Sheats advised he didn\'t know where he was coming from, but he was going home.I next asked Mr. Sheats to advise his alphabet starting from the letter "D" to the letter "Z" without singing. On Mr. Sheats first attempt he started at the letter "A" and upon coming to the letter "D" he began to recite his numbers. He was stopped, readvised the instructions, and asked to recite the exercise again. Mr. Sheats second attempt resulted the same as the first. A third time Mr. Sheats was advised again, and resulted in the same results as the first and second. Finally, I read Mr. Sheats his Georgia Implied Consent verbatim, which he consented to take a test through breath analysis.Mr. Sheats was transported to Georgia Tech police station in order to conduct a breath analysis. During the transport to the location, Mr. Sheats continued to apologize and claimed he was innocent for he was not capable of doing wrong. Mr. Sheats uttered over and over his previous time in federal prison, his vehicle tag number, and how he couldn\'t afford to get into trouble with his wife and kids. Upon reaching Georgia Tech police Mr. Sheats inquired if I could let him go home after the testing was completed with his citations. Mr. Sheats was tested by myself (Permit #40102) with a test sample of .267Grams and .264Grams.Upon receiving his appropriate documents Mr. Sheats\'s demeanor became aggressive and angry. He began to make a personal argument about his family, claiming himself to be a "G" (gangster), and how he was wronged by the system. However, he was transported to Atlanta Detention Center with no incident. Mr. Sheats was charged: Failure to Obey Traffic Control Device, Driving With No License, Open Beverage Container, DUI/Less Safe/Alcohol, Reckless Driving, and DUI/Alcohol > 0.08Grams. Mr. Sheats vehicle was impounded by S&W Towing.  Supervisor Unit #1194 (Sgt. G. Nelms) was notified of the above incident.END OF REPORT', 'update_date': 1357020053, 'id': u'130010093'}, {'remarks': u"     On January 1, 2013 at approximately 12:20 a.m., I, Officer Drinkard was dispatched to 1631 Stanton Road SW on a person down call. On scene, Grady Unit #332 was preparing to transport the victim, Mr. William Johnson.  An unknown witness stated he saw the suspect strike the victim in the face two times with a closed fist and then strike him in the head with a glass bottle. The witness advised that both parties had been drinking which played a part in the turn of events. The witness stated the suspect lived in Building N at the top tier of the building. I asked the witness to accompany me to the location of the building. While on the way there the witness stated the suspect drove a two door, white in color Chevy Monte Carlo.As we made our way to the apartment I observed a two door, white in color Chevy Monte Carlo backing up and attempting to leave the location. The only entrance and exit was slightly blocked by the Grady Unit as well as my Unit vehicle. The Monte Carlo was traveling at a high rate of speed within the apartment complex in an attempt to exit. I ran over and stopped the vehicle. I asked the driver for his driver's license. The driver attempted to retrieve his license from his wallet which he had pulled from his blue jean pants pocket. The vehicle kept rocking back and forth due to the slight elevation of the hill which we were on. I repositioned myself from the driver's side to more in front of the vehicle close to the driver's side fender. I asked the driver to put the vehicle in park and turn the vehicle off. At this time the driver looked up at me, dropped his wallet, turned the wheel in my direction and attempted to strike me in his haste to flee the scene.I jumped back and struck the vehicle with my hand as I ordered him to stop the vehicle yet again. I retrieved the tag information from the vehicle and immediately put a lookout out over radio for the vehicle description and Georgia Tag #BZL1884 and direction of travel. The vehicle came back to an Angela Campbell of Mableton, Georgia. There were two black males in the vehicle. The driver had on blue jeans, dark colored t-shirt, jacket, a tan fitted cap and mardi gras beads around his neck. The passenger had on blue jeans and a burgundy jacket. The caller was Jessica (404) 749-0211. Sergeant Benson #1496 copied the call as well Sargent Hines #1494. A General Investigator #4381 was notified of the call as well.I went to Grady to follow up with the victim. The victim was not cooperative at all. He did not want to give his biographical information. He did not want to provide any vital information to his case. He did not advise the name of his assailant either. There is nothing further at this time. ***END OF REPORT***", 'update_date': 1357019208, 'id': u'130010103'}, {'remarks': u'I was dispatched to a call at 3350 Greenbriar Pkwy Sw on 01/01/13. Upon my arrival, I spoke with the victim who stated that the rear window of her vehicle had been shattered. It appeared that the vehicle had been struck by a stray bullet from a handgun that had been fired on the night of New Years Eve. The victim was not with the vehicle at the time that the incident occurred and there were no injuries. ', 'update_date': 1357865421, 'id': u'130010121'}, {'remarks': u"On Tuesday January 1st, 2013 I, Ofc M. Vermillion, was patrolling the area of 80 Forsyth St when I saw Mr. Travis Monroe commit the offense of disorderly conduct.  While travelling down Forsyth St. I heard yelling in front of the Rialto at 80 Forsyth St.  When I looked I saw Mr. Monroe yelling at a man with two females who was walking away from him down the street.  I then saw Mr. Monroe reach into his coat pocket and pull out his hand quickly in a motion consistent with holding a gun.  He then used his empty hand to make several gestures of gunshots.  I then stopped Mr. Monroe and asked what was going on.  He stated that it was just some people in a disagreement.  I left Mr. Monroe with my partner, Ofc. M. Stenson, and went to talk to the other party involved.  I caught up with Mr. Casmiero Canionero and asked him what happened.  He stated that while walking in the opposite direction he passed Mr. Monroe on the sidewalk.  Mr. Canionero stated that Mr. Monroe made an obscene advance at Mr. Canionero's daughter.  Mr. Canionero told him not to do that and leave them alone.  Mr. Canionero stated that then Mr. Monroe began yelling that he was going to kick his ass and shoot him and then made the shooting gesture.  I returned to my partner and we placed Mr. Monroe in handcuffs for the offense of Disorderly Conduct.  Mr. Monroe resisted the handcuffs trying to pull his hands away.  We then attempted to place Mr. Monroe in the back of the wagon.  Mr. Monroe resisted by pushing off the back of the wagon with his feet and refusing to step inside.  I then grabbed Mr. Monroe and laid him down in the back of the wagon and slid him in.  As I let go Mr. Monroe kicked violently at myself and Ofc Stenson before we shut the door.  He was then transported to city jail and his property was placed in property control.", 'update_date': 1357005745, 'id': u'130010258'}]
	#print keywords
	#print "matched items by keyword:", matched_items, len(matched_items)



	# similarity_matrix = [ [1.0,0.1,0.2,0.4,0.7],
	# 					  [0.1,1.0,0.3,0.5,0.8],
	# 					  [0.2,0.3,1.0,0.6,0.9],
	# 					  [0.4,0.5,0.6,1.0,1.0],
	# 					  [0.7,0.8,0.9,1.0,1.0]]
	# for i in range(len(matched_items)):
	# 	matched_items[i]["similarity"] = similarity_matrix[i]

	# print matched_items
	# similarity_matrix = f.get_similarity_matrix(id_vector)
	#a = f.query_via_id(id_vector[0],0)



	return json.dumps({
		"status": 0,
		"res": matched_items
		})



# API for getting basic info via crime ids
@app.route("/getBasicInfos", methods=["POST"])
def getBasicInfos():
	crime_ids = []
	# Parse requested parameters
	if request.method == "POST":
		para_dict = json.loads(request.data)
		crime_ids = para_dict["crimeIds"]
	else:
		return json.dumps({
			"status": 1,
			"msg": "Invalid Request Type"})
	
	basic_infos = basic_info_handler.get("incident_num", crime_ids)
	if basic_infos == None or basic_infos == []:
		return json.dumps({
			"status": 0,
			"res": []})

	return json.dumps({
		"status": 0,
		"res": [{
			"id": basic_info["id"],
			"city": basic_info["city"],
			"date": basic_info["date"],
			"priority": basic_info["priority"],
			"label": basic_info["category"],
			"position": { "lat": basic_info["avg_lat"], "lng": -1 * basic_info["avg_long"] }}
			for basic_info in basic_infos]})



# API for getting remarks and updated date via crime id
@app.route("/getReportRemarks", methods=["POST"])
def getReportRemarks():
	crime_ids = []
	# Parse requested parameters
	if request.method == "POST":
		para_dict = json.loads(request.data)
		crime_ids = para_dict["crimeIds"]
	else:
		return json.dumps({
			"status": 1,
			"msg": "Invalid Request Type"})

	report_texts = report_text_handler.get("incident_num", crime_ids)
	if report_texts == None or report_texts == []:
		return json.dumps({
			"status": 0,
			"res": []})

	# update_date = report_texts["update_date"]
	# remarks     = report_texts["remarks"]
	return json.dumps({
		"status": 0,
		"res": report_texts})

