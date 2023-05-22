# sqlalchemy-challenge

* climate_starter.ipnyb

    *   Precipitation Analysis - Queries and plots date and precipitation values for previous 12 months of data
    *   Station Analysis
        *   Shows total # of stations
        *   Queries max,min, and avg temperatures for the most active3 station
        *   Queries and plots the previous 12 months of TOBS data for the most active station


* app.py

    *   Create a Flask application with the following routes:
        *   A precipitation route that:
            *   Returns json with the date as the key and the value as the precipitation
            *   Only returns the jsonified precipitation data for the last year in the database
        *   A stations route that:
            *   Returns jsonified data of all of the stations in the database
        *   A tobs route that:
            *   Returns jsonified data for the most active station
            *   Only returns the jsonified data for the last year of data
        *   A start route that:
            *   Accepts the start date as a parameter from the URL
            *   Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
        *   A start/end route that:
            *   Accepts the start and end dates as parameters from the URL
            *   Returns the min, max, and average temperatures calculated from the given start date to the given end date
