# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite://///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.metadata.create_all(engine)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

@app.route("/")
def home():
    return(
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/2010-01-10<br/>"
    f"/api/v1.0/<start>/2010-01-10/2017-08-23'")


#################################################
# Flask Routes
#################################################

#precipitation analysis 

# Define the /api/v1.0/precipitation route

@app.route('/api/v1.0/precipitation')
def precipitation():

    session = session(engine)

    # Convert the precipitation DataFrame to a dictionary
    precipitation_dict = precipitation_df.set_index('Date')['Precipitation'].to_dict()
    return jsonify(precipitation_dict)

    # Create a query to collect date and precipitation for the last year of data
query = f"SELECT date, prcp FROM measurement WHERE date = 2017-08-23, '-1 year')"

# Execute the query and save the results to a Pandas DataFrame
df = pd.read_sql_query(query, engine)

# Sort the DataFrame by date
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# Plot the results
df.plot(x='date', y='prcp', legend=False)
plt.xlabel('Date')
plt.ylabel(inches')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Use Pandas to print the summary statistics for the precipitation data
precipitation_stats = df['prcp'].describe()
print(precipitation_stats)

#closing session
 session.close()



#Station Analysis

@app.route("/api/v1.0/stations")
def stations():

# Query to Find the Number of Stations
station_count = session.query(func.count(func.distinct(measurement.station))).scalar()

# Query to List Stations and Observation Counts
station_observations = session.query(measurement.station, func.count(measurement.station).label('observation_count')) \
    .group_by(measurement.station) \
    .order_by(func.count(measurement.station).desc())

most_active_station = station_observations.first()  # The most active station will be the first result

# Query to Find Min, Max, and Average Temperatures for the Most Active Station
most_active_station_id = most_active_station.station
temp_stats = session.query(func.min(measurement.tobs).label('min_temperature'),
                           func.max(measurement.tobs).label('max_temperature'),
                           func.avg(measurement.tobs).label('avg_temperature')) \
    .filter(measurement.station == most_active_station_id).first()

# Query to Get Previous 12 Months of TOBS Data for the Most Active Station
most_active_station_tobs = session.query(measurement.date, measurement.tobs) \
    .filter(measurement.station == most_active_station_id) \
    .filter(measurement.date >= func.date((func.strftime("%Y", func.max(measurement.date)) + '-01-01'), '-12 months')).all()

# Save the Query Results to a Pandas df
tobs_df = pd.DataFrame(most_active_station_tobs, columns=['Date', 'Temperature'])

# Plot a Histogram with Bins=12
tobs_df.plot(kind='frequency', y='Temperature', bins=12)
plt.xlabel('Temperature (°F)')
plt.ylabel('Frequency')
plt.show()

# Close the session
session.close()
