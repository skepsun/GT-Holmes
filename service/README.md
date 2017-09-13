# Crime-Pattern-Detection Service Folder
### Introduction
The service folder in the Crime-Pattern-Detection project contains several files that build a system to fetch data from database and demonstrate crime incidents correlation detection results. It contains database wrapper, date visualization, full text search and many other features to demonstrate the incident correlation detection results. Below is an illustration for the structure of the service folder. 

![service folder structure](https://github.com/meowoodie/Crime-Pattern-Detection-for-APD/blob/Suyi/service/img/service_folder_structure.png)
*<div align=center>Structure of service folder.</div>*

The folder mainly contains three components:

-	Database wrapper: it provides restful API to connect the database and parse the retrieved data to JSON format.
- View component: it provides functions to process the retrieved data from the database according to the user input.
- Front end: it provides functions to render a web page, on which we can show the detection results. Also, we can receive user input from the webpage.

### Database Wrapper

Database wrapper provides functions to connect the database and fetch data. The data streams that we received from database wrapper have uniform data structures for easier data information extraction.
Usually items of the data stream from database wrapper can be defined as follows:
```
{
  "id":       incident_num,
  "avg_lat":  avg_lat,
  "avg_long": avg_long,
  "city":     city,
  "date":		date,
  "priority": priority,
  "category": category,
  "incident_date_timestamp": incident_date_timestamp
}
```
```
{
  "id":          incident_num,
  "update_date": update_date,
  "remarks":     remarks
  }
```

### View Component

The view component would extract the information of the payload. Then the extracted data might be processed by the data model. Finally, the result which consists of "statue" and "res" will be sent to front end HTML page. Below is the illustration:
```
{
  "status": 0,
  "res": [{
    "id": filter_ids[ind], 
    "similarity": float(sims[ind]), 
    "label": categories[ind],
    "position": { "lat": positions[ind][0], "lng": -1 * positions[ind][1] },
    "city": cities[ind],
    "priority": priorities[ind],
    "update_dates": update_dates[ind],
    "date": dates[ind],
    "text": remarks[ind] }
    for ind in range(len(filter_ids))
    if len(ids[ind]) >= 9 ]
    }
```
### Front End
The front end web page provides several visualization functions to demonstrate the incident correlation detection results.

#### Demonstrate incidents on the map
<br>Each dot represents a crime incident with real location.</br>
<div align=center><img src="https://github.com/meowoodie/Crime-Pattern-Detection-for-APD/blob/Suyi/service/img/dots_on_map.gif"/></div>

*<div align=center>Demonstrate incidents on the map.</div>*

#### Represent similarities using dot size
Larger dots mean incidents with higher similarities.
<div align=center><img width=360 height=210 src="https://github.com/meowoodie/Crime-Pattern-Detection-for-APD/blob/Suyi/service/img/biggerdots.jpg"/></div>

*<div align=center>Represent similarities using dot size.</div>*

#### Represent similarities using lines
Darker lines mean higher similarties between incidents.
<div align=center><img src="https://github.com/meowoodie/Crime-Pattern-Detection-for-APD/blob/Suyi/service/img/dots.gif"/></div>

*<div align=center>Represent similarities using lines.</div>*
