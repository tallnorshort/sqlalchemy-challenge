# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():

    # """List all available api routes."""
    return (
        f"Available Routes for climate analysis!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Find last date in database
    Last_Year_Observation = dt.date(2017, 8, 23) - dt.timedelta(days=7*52)

    Last_Year_Observation

    # Query all passengers
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > Last_Year_Observation).all()
    
    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []

    for date_ob in results:
        all_tobs_dict = {}
        all_tobs_dict["Date"] = date_ob.date
        all_tobs_dict["Temperature"] = date_ob.tobs

        all_tobs.append(all_tobs_dict)
    
    # Jsonify all_tobs
    return jsonify(all_tobs)

# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stationName():
    # Query all station names
    stationName_results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stationName_list = list(np.ravel(stationName_results))

    # Jsonify all_tobs
    return jsonify(stationName_list)

# Return a JSON list of Temperature Observations (tobs) for the previous year

@app.route("/api/v1.0/tobs")
def tobs():
    #Find last date in database
    Last_Year_Observation = dt.date(2017, 8, 23) - dt.timedelta(days=7*52)

    Last_Year_Observation

    # Query temp observations
    tobs_results = session.query(Measurement.tobs).filter(Measurement.date > Last_Year_Observation).all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    # Jsonify all_tobs
    return jsonify(tobs_list)


# /api/v1.0/<start>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(day_temp_results)


# /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(multi_day_temp_results)

if __name__ == "__main__":
    app.run(debug=True)