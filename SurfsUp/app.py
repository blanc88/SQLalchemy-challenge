# Import the dependencies.
import numpy as np 
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 


#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect = True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station 

# Create our session (link) from Python to the DB

session = Session(engine)



#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        "Welcome to the homepage. Available routes:\n"
        "/api/v1.0/precipitation\n"
        "/api/v1.0/stations\n"
        "/api/v1.0/tobs\n"
        "/api/v1.0/<start>\n"
        "/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    prep_scores = session.query(Measurement.date, Measurement.prcp).all()

    precipitation = []
    for date, prcp in prep_scores:
        precipitationDict = {}
        precipitationDict["date"] = date
        precipitationDict["precipitation"] = prcp 
        precipitation.append(precipitationDict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    total_stat = session.query(Station.station, Station.name).all()

    stations = []
    for station, name in total_stat:
        stationDict = {}
        stationDict["station"] = station 
        stationDict["name"] = name 
        stations.append(stationDict)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():


    most_act_stat = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
                    .group_by(Measurement.station)\
                    .order_by(func.count(Measurement.tobs).desc()).first()[0]
    
    twelve_month_data = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
                        .filter(Measurement.station == most_act_stat)\
                        .filter(Measurement.date >= twelve_month_data).all()
    

    tobs_ = []
    for date, station, tobs in twelve_month_data:
        tobsDict = {}
        tobsDict["date"] = date
        tobsDict["station"] = station
        tobsDict["tobs"] = tobs
        tobs_.append(tobsDict)

    return jsonify(tobs_)




    session.close()




if __name__ == "__main__":
    app.run(debug=True)