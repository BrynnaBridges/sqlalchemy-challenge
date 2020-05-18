import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Set up Flask
app = Flask(__name__)

#List all routes that are available.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(measurement.station).distinct().all()

    session.close()

    # Convert into list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session
    session = Session(engine)

    """Return a list of last years temperatures"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(measurement.tobs).\
    filter(func.strftime('%Y-%m-%d', measurement.date) >= "2016-08-23").\
    filter((measurement.station) == 'USC00519281').all()

    session.close()

    # Convert into list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)



if __name__ == '__main__':
    app.run(debug=True)


