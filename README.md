# Tempus

This depository contains the project for CS481 Dava Visualization course offered at KAIST in Spring 2023. 

Important: IN the planning page, requests to ChatGPT take 15-20 to process. This limitation is entirely due to OpenAI API and there's little that can be done here. Also, the code was tested on VM running windows. It is not guaranteed to run correctly on UNIX-based OS.

## Members - [Group 2] Team 4 - Tempus
- ChinWei Huang
- Washik Uddin Ahmed Mollah
- Nikolai Kurlovich

## Execution
Our project is currently deployed on heroku and can be accessed at: https://tempus2.herokuapp.com. If you wish you install our project on your local machine, please follow this guidelines. Please install all the python requirments and then execute index.py file. This can be done as follows:

```bash
pip install -r requirements.txt
python index.py
```

## Folder structure
```
+-- app.py: Dash app server
+-- components : Separate folder for the nav. bar
|   +-- navbar.py : Navigation bar component
+-- index.py : Overall App layout 
+-- pages : Pages
|   +-- data : this folder contains the data we use
|   +-- main.py : main page (/)
|   +-- analysis.py : analysis page
|   +-- suggest.py : page with schedule suggestions
|   +-- plan.py : page which allows user to create his or her schedule for the next day
|   +-- use.py : page which allows user to compare what he planned vs what was actually done
```