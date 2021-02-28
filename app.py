#import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

#save reference to the table
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= query_date).order_by(Measurement.date.desc()).all()
    session.close()

    # Create a dictionary from the row data and append to a list
    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_data.append(precip_dict)
    
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurement.station).distinct().all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.date >= query_date).filter(Measurement.station=="USC00519281").all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def temperature(start=None,end=None):
    session = Session(engine)
    if end==None:
        results = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.station=="USC00519281"),func.max(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.station=="USC00519281"),func.avg(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.station=="USC00519281")).all()
    else:
        results = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.station=="USC00519281"),func.max(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.station=="USC00519281"),func.avg(Measurement.tobs).filter(Measurement.date >= start,Measurement.date <= end).filter(Measurement.station=="USC00519281")).all()
    session.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

