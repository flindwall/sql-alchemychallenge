import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import flask
from flask import Flask , jsonify

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect existing database into new model and reflect tables
Base = automap_base()
Base.prepare(engine, reflect = True)
#print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

#create app using Flask
app = Flask(__name__)

#define routes that user could take
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#Convert the query results from your precipitation analysis
#to a dictionary using date as the key and prcp as the value
#return JSON representation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >=('2016-08-23')).\
    order_by(Measurement.date).all()

    session.close()
    return jsonify(dict(prcp_results))


#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.stations).all()

    session.close()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year
@app.route("/api/v1.0/tobs")
def most_active_temp():
    session = Session(engine)
    temp_results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= ('2016-08-23')).\
                    order_by(Measurement.date).all()
    session.Close()
    return jsonify(dict(temp_results))


#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0<start>")
def temp(start_date):
    session = Session(engine)
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    min_temp = session.query(func.min(Measurement.tobs)).filter().all(Measurement.date >= start_date).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter().all(Measurement.date >= start_date).all()

    session.Close()
    return(jsonify({"Minimum Temperature" : min_temp, "Maximum Temperature": max_temp, "Average Temperature" : avg_temp}))
    
@app.route("/api/v1.0/<start>/<end>")
def temps(start_date, end_date):
    session = Session(engine)
    max_temps = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    min_temps = session.query(func.min(Measurement.tobs)).filter().all(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    avg_temps = session.query(func.avg(Measurement.tobs)).filter().all(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.Close()
    return(jsonify({"Minimum Temperature" : min_temps, "Maximum Temperature": max_temps, "Average Temperature" : avg_temps}))
    

    
if __name__ == '__main__':
    app.run(debug=True)
    










