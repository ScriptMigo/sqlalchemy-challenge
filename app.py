import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/stations")
def stations():
    # Query list of stations and counts
    results = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()

    # Convert the query results to a list of stations inside Dicitonary
    allStations=[]
    for row in results:
        stations = {}
        stations["station"] = row[0]
        stations["count"] = row[1]
        allStations.append(stations)

    return jsonify(allStations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    allPrecip = []
    for precip in results:
        precipDict = {}
        precipDict["date"] = precip.date
        precipDict["prcp"] = precip.prcp
        allPrecip.append(precipDict)

    return jsonify(allPrecip)
	
@app.route("/api/v1.0/<start>")
def tempsStart(start):
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    tobs=[]
    for row in results:
        tobsDict = {}
        tobsDict["TMIN"] = row[0]
        tobsDict["TAVG"] = row[1]
        tobsDict["TMAX"] = row[2]
        tobs.append(tobsDict)

    return jsonify(tobs)


@app.route("/api/v1.0/tobs")
def tobs():
    lastDate=session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    for date in lastDate:
        lastDate=date.split('-')
    
    lastYear=int(lastDate[0])
    lastMonth=int(lastDate[1])
    lastDay=int(lastDate[2])
    
    queryDate = dt.date(lastYear, lastMonth, lastDay) - dt.timedelta(days=365)
    
    # Query list of stations and counts
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date>=queryDate).\
                order_by(Measurement.date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    last12Tobs=[]
    for row in results:
        tobs = {}
        tobs["date"] = row.date
        tobs["station"] = row.tobs
        last12Tobs.append(tobs)

    return jsonify(last12Tobs)


@app.route("/api/v1.0/<start>/<end>")
def tempsStartEnd(start, end):
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    startEndTobs=[]
    for row in results:
        tobs = {}
        tobs["TMIN"] = row[0]
        tobs["TAVG"] = row[1]
        tobs["TMAX"] = row[2]
        startEndTobs.append(tobs)

    return jsonify(tobs)


if __name__ == '__main__':
    app.run(debug=True)
