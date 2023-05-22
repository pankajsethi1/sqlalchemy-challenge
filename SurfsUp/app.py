# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()

# Save references to each table
Measurement =  Base.classes.measurement
Station =  Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# List all available api routes..
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )


# Display last 12 months of precipitation data when user hits the /api/v1.0/precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    date_one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= date_one_year_ago).all()
    session.close()

    # Create a dictionary from the results data and append to a list of prec_data
    prec_data = []
    for date, prec in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["prec"] = prec
        prec_data.append(prec_dict)

    return jsonify(prec_data)

# Display list of stations when the user hits the /api/v1.0/stations route

@app.route("/api/v1.0/stations")
def stations():
    # Query the stations in the dataset
    results=session.query(Station.id,Station.name).all()
    session.close()
    # Create a dictionary from the results data and append to a list of station_data
    station_data = []
    for id,name in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["name"] = name
        station_data.append(station_dict)

    return jsonify(station_data)

# Display the dates and temperature observations of the most-active station for the previous year of data
# when the user hits the /api/v1.0/tobs route

@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most active station
    most_active_station = session.query(Measurement.station,func.count(Measurement.station))\
        .group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()[0][0]
    # Query date and precipitation data for the most active station only for last year
    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= dt.date(2017,8,23) - dt.timedelta(days=365)).all()
    session.close()
    # Create a dictionary from the results data and append to a list of prec_data
    prec_data = []
    for date, prec in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["prec"] = prec
        prec_data.append(prec_dict)

    return jsonify(prec_data)

# Display min,avg and max for date>=start when the user hits the /api/v1.0/start/<start> route

@app.route("/api/v1.0/start/<start>")
def start_date_temp(start):
    # Find min,avg and max for date>=start
    results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).all()
    session.close()
    # Create a list of dictionary from the results data
    temp_data =[{"min":results[0][0],"avg":results[0][2],"max":results[0][2]}]
    return jsonify(temp_data)

# Display min,avg and max for date>=start and data<=end when the user hits 
# the /api/v1.0/start/end/<start>/<end> route

@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end_date_temp(start,end):
    # Find min,avg and max for date>=start and date<=end
    results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).filter(Measurement.date <=end).all()
    session.close()
    # Create a list of dictionary from the results data
    temp_data =[{"min":results[0][0],"avg":results[0][2],"max":results[0][2]}]
    return jsonify(temp_data)

################################################# 
# Define main behavior
#################################################
if __name__ == "__main__":
    app.run(debug=True)


