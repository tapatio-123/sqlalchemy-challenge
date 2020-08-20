
import numpy as np

import sqlalchemy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurements = Base.classes.measurement


app = Flask(__name__)

@app.route("/")
def home():
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
    session = Session(engine)
    results = session.query(measurements.date, measurements.prcp)

    session.close()

    all_data = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        all_data.append(prcp_dict)

    return jsonify(all_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(measurements.station)
    session.close()

    data = []
    for station in results:
        stat_dict={}
        stat_dict["station"] = station
        data.append(stat_dict)
    return jsonify(data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    twelve_months_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurements.date, measurements.tobs, measurements.station)\
        .filter(measurements.station=='USC00519281').filter(measurements.date>=twelve_months_ago).all()

    session.close()

    tob = []
    for dates, tobs, station in results:
        tobs_dict={}
        tobs_dict["station"] = station
        tobs_dict["date"] = dates
        tobs_dict["tobs"] = tobs
        
        tob.append(tobs_dict)

    return jsonify(tob)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    results = session.query(func.min(measurements.tobs), func.avg(measurements.tobs),func.max(measurements.tobs)\
        .filter(measurements.date >= start)).all()
    session.close()
 

    first_list = []
    for min, avg, max in results:
        date_dict={}
        date_dict["min temp"] = min
        date_dict["avg temp"] = avg
        date_dict["max temp"] = max
        first_list.append(date_dict)


    return jsonify(first_list)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)
    results = session.query(func.min(measurements.tobs), func.avg(measurements.tobs),func.max(measurements.tobs)\
        .filter(measurements.date >= start).filter(measurements.date <= end) ).all()
    session.close()
 

    first_list = []
    for min, avg, max in results:
        date_dict={}
        date_dict["min temp"] = min
        date_dict["avg temp"] = avg
        date_dict["max temp"] = max
        first_list.append(date_dict)

    return jsonify(first_list)



if __name__ == "__main__":
    app.run(debug=True)