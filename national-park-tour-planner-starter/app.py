from flask import Flask, render_template, request, jsonify
import logging
from datetime import datetime
from langchain_core.prompts import PromptTemplate

# app will run at: http://127.0.0.1:5000/

# Initialize logging
logging.basicConfig(filename="app.log", level=logging.INFO)
log = logging.getLogger("app")

# prompt
def build_new_trip_prompt(form_data):
  prompt_template = PromptTemplate.from_template("You are a trip advisor who will provide an itinerary for each day of the trip ranging from {trip_start} to {trip_end} for someone who is traveling {traveling_with_list} to {location}. They are interested in lodging in {lodging_list} and planning activities that could include {adventure_list} also plan one suggested meal per day.")
  return prompt_template.format(
    location = form_data["location"],
    trip_start = form_data["trip_start"],
    trip_end = form_data["trip_end"],
    traveling_with_list = form_data["traveling_with_list"],
    lodging_list = form_data["lodging_list"],
    adventure_list = form_data["adventure_list"] 
  )

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
  
# Define the route for the plan trip page
@app.route("/plan_trip", methods=["GET"])
def plan_trip():
  return render_template("plan-trip.html")

# Define the route for view trip page with the generated trip itinerary
@app.route("/view_trip", methods=["POST"])
def view_trip():
  # log.info(request.form)
  traveling_with_list = ", ".join(request.form.getlist("traveling-with"))
  lodging_list = ", ".join(request.form.getlist("lodging"))
  adventure_list = ", ".join(request.form.getlist("adventure"))

  cleaned_form_data ={
     "location": request.form["location-search"],
     "trip_start": request.form["trip-start"],
     "trip_end": request.form["trip-end"],
     "traveling_with_list": traveling_with_list,
     "lodging_list": lodging_list,
     "adventure_list": adventure_list,
     "trip_name": request.form["trip-name"]
  }

  # log.info(cleaned_form_data)

  prompt = build_new_trip_prompt(cleaned_form_data)
  log.info(prompt)
  return render_template("view-trip.html")
    
# Run the flask server
if __name__ == "__main__":
    app.run()
