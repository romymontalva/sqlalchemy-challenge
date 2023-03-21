import datetime as dt
import nunpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine["sqlite:///Resources/hawaii.sqlite"]

Base = automap_base()
Base.prepare(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

Session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/av1.0/stations<br/>"
        f"/api/av1.0/tobs<br/>"
        f"/api/av1.0/temp/start<br/>"
        f"/api/av1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYY.</p>"
    )
@app.route("/api/v1.o/precipitation")
def precipiration():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    session.close()
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

@app.route("/api/avi.0/stations")
def stations():
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_tear = dt.date(2017, 8 ,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
       filter(Measurement.station == 'USC0051918281').\
       FILTER(Measurement.date >= prev_year).all()
    
    session.close()


    print()

    temps= list(np.ravel(results))

    return jsonify({ temps: temps})

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m%d%y")
        results = session.query(*sel).\
           filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps)

    start = dt.datetime.strptime(start, "%m%d%y")
    end = dt.datetime.strptime(end, "%m%d%y")

    results = session.query(*sel).\
       filter(Measurement.date >= start).\
       filter(Measurement.date <= end).all()
    print(start)
    print(end)
    print(results)

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)





    


if __name__ == "__main__":
    app.run(debug=True)