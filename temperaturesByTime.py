def temperaturesByTime(razredi=[(-100,100)],filename='',method=1, returnShape='both'):
    """
    This function read the ARSO data, 
    parses it based on the daily or hourly method and returns an
    array of values based on the predetermined temperature classes
    Parameters:
        razredi - temperaturni razredi, an array of tuples
        filename - the name of the ARSO csv placed into the root
        method - 0: daily, 1:hourly
    """
    # Initialize Results Array. First value is average temp of the razred,
    # second is the amount of time
    resultsArray = list(map(lambda x: [(x[0]+x[1])/2,0], razredi))
    # First we prepare the array of measurements
    measurements = []
    with open(filename) as file:
        # First we prepare the array of items
        for index, line in enumerate(file):
            if index == 0:
                #We remove the header row
                continue;
            measurements.append(line.split(";")[:4])
    def addToResultsArray(temperature):
        """
        This function iterates the correct place in the results array by one.
        """
        for i, r in enumerate(razredi):
                # We check for each razred if the measured temperature fits
                if( r[0] < temperature and temperature <= r[1] ):
                    # The measuremed temperature fits the razred, we add one
                    # hour to the correct place in results array
                    resultsArray[i][1] += 1
    def returnData():
        """
        This function formats the data to be returned
        """
        if(returnShape == 'temperature'):
            return list(map(lambda x: x[0], resultsArray))
        if(returnShape == 'time'):
            return list(map(lambda x: x[1], resultsArray))
        if(returnShape == 'both'):
            return resultsArray
        return resultsArray
            
    # If we are using hourly method
    if( method == 1):
        for m in measurements:
            # Now we put the measurement into the correct place in the results array
            addToResultsArray(float(m[3]))
        return returnData()
    # If we are using daily method
    if( method == 0 ):
        # We agregate hourly values for each day
        dailyAgregate = 0
        for m in measurements:
            # Add the temperature to the daily agregate
            dailyAgregate = dailyAgregate + float(m[3])
            # If we have reached the last hour
            if( float(m[2]) == 23 ):
                # Get the daily average temperature
                dailyAgregate /= 24
                # Add a value to the results
                addToResultsArray(dailyAgregate)
                # Reset daily agregate
                dailyAgregate = 0
        # We have finished the for loop
        return returnData()