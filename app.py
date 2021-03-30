import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///./Resources/hawaii.sqlite", echo=False)
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)


@app.route('/')
def home():
    return (f'Hawaii Weather/Station API<br>'
            f'For the last 12 months of precipitation data use: /api/v1.0/precipitation<br>'
            f'For a full list of stations use: /api/v1.0/stations<br>'
            f'For the temperatures of the most active station use: /api/v1.0/tobs<br>'
            f'To search for min, max, and average temperatures from a given start date use: /api/v1.0/"startdate"<br>'
            f'To search for min, max, and average temperatures between 2 dates use: /api/v1.0/"startdate"/"enddate"')


@app.route('/api/v1.0/precipitation')
def prcp():
    data = session.query(Measurement.prcp, Measurement.date).filter(
        Measurement.date > '2016-08-23').order_by(Measurement.date).all()

    prcp_df = []
    for p, d in data:
        prcp_dict = {}
        prcp_dict["date"] = d
        prcp_dict["precipitaion"] = p
        prcp_df.append(prcp_dict)

    session.close()

    list(np.ravel(prcp_df))
    return jsonify(prcp_df)


@app.route('/api/v1.0/stations')
def stations():
    data = session.query(Station.id, Station.station, Station.name,
                         Station.latitude, Station.longitude, Station.elevation).all()

    station_df = []
    for iD, st, name, lat, lon, ele in data:
        station_dict = {}
        station_dict['id'] = iD
        station_dict['station'] = st
        station_dict['name'] = name
        station_dict['latitude'] = lat
        station_dict['longitude'] = lon
        station_dict['elevation'] = ele
        station_df.append(station_dict)

    session.close()

    list(np.ravel(station_df))
    return jsonify(station_df)


@app.route('/api/v1.0/tobs')
def tobs():
    data = session.query(Measurement.station, Station.name, Measurement.tobs,
                         Measurement.date).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').all()

    tobs_df = []
    for st, name, tobs, date in data:
        tobs_dict = {}
        tobs_dict['station'] = st
        tobs_dict['name'] = name
        tobs_dict['tobs'] = tobs
        tobs_dict['date'] = date
        tobs_df.append(tobs_dict)

    session.close()

    list(np.ravel(tobs_df))
    return jsonify(tobs_df)


@app.route('/api/v1.0/<start>')
def startDate(start):
    data = session.query(func.min(Measurement.tobs), func.max(
        Measurement.tobs), func.avg(Measurement.tobs), Measurement.date).group_by(Measurement.date).filter(Measurement.date >= start).all()

    start_df = []
    for a, b, c, date in data:
        start_dict = {}
        start_dict['minTemp'] = a
        start_dict['maxTemp'] = b
        start_dict['averageTemp'] = c
        start_dict['date'] = date
        start_df.append(start_dict)

    session.close()

    list(np.ravel(start_df))
    return jsonify(start_df)


@app.route('/api/v1.0/<start>/<end>')
def startEnd(start, end):
    data = session.query(func.min(Measurement.tobs), func.max(
        Measurement.tobs), func.avg(Measurement.tobs), Measurement.date).group_by(Measurement.date).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    startend_df = []
    for a, b, c, date in data:
        startend_dict = {}
        startend_dict['minTemp'] = a
        startend_dict['maxTemp'] = b
        startend_dict['averageTemp'] = c
        startend_dict['date'] = date
        startend_df.append(startend_dict)

    session.close()

    list(np.ravel(startend_df))
    return jsonify(startend_df)


if __name__ == "__main__":
    app.run(debug=True)
