import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/"
        f"enter start date"
        f"(date must be in format yyyy-mm-dd)<br/>"
        f"....example: /api/v1.0/2015-04-25<br/>"
        f"/api/v1.0/"
        f"enter start date/end date"
        f"(date must be in format yyyy-mm-dd)<br/>"
        f"....example: /api/v1.0/2015-04-25/2016-04-25<br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    #2) get a list of precipitation
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stations():
    #3) get a list of stations
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs_yr():
    #4) tobs for USC00519281 for last year
    start_point = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    session = Session(engine)
    tobs_yr = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= start_point).all()
    session.close()

    results = list(np.ravel(tobs_yr))

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_date(start):
    #5) return the min, avg and max temperature from a variable start date to the end of data
    session = Session(engine)
    start_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()

    results = list(np.ravel(start_query))

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    #5) return the min, avg and max temperature from a variable start date to a variable end date
    session = Session(engine)
    start_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

    results = list(np.ravel(start_query))

    return jsonify(results)




if __name__ == '__main__':
    app.run(debug=True)
