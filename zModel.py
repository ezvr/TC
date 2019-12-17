def temperaturesByTime(razredi=[(-100, 100)], filename='meteorological_year_ljubljana.csv', method='daily', returnShape='all'):
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
    resultsArray = list(map(lambda x: [(x[0]+x[1])/2, 0, 0], razredi))
    # First we prepare the array of measurements
    measurements = []
    with open(filename) as file:
        # First we prepare the array of items
        for index, line in enumerate(file):
            if index == 0:
                # We remove the header row
                continue
            measurements.append(line.split(";")[:6])

    def addToResultsArray(temperature, radiation):
        """
        This function iterates the correct place in the results array by one.
        """
        for i, r in enumerate(razredi):
                # We check for each razred if the measured temperature fits
            if(r[0] < temperature and temperature <= r[1]):
                # The measuremed temperature fits the razred, we add one
                # hour to the correct place in results array
                resultsArray[i][1] += 1
                resultsArray[i][2] += radiation

    def returnData():
        """
        This function formats the data to be returned,
        using a map function to prepare the returned array
        """
        # If the method is daily, we must get the average of the
        # daily radiations. So we divide by all the days.
        if(method == 'daily'):
            for i, r in enumerate(resultsArray):
                # Check to not divide by zero
                if(resultsArray[i][1] != 0):
                    resultsArray[i][2] /= resultsArray[i][1]
        if(returnShape == 'temperature'):
            return list(map(lambda x: x[0], resultsArray))
        if(returnShape == 'time'):
            return list(map(lambda x: x[1], resultsArray))
        if(returnShape == 'radiation'):
            return list(map(lambda x: x[2], resultsArray))
        if(returnShape == 'all'):
            return resultsArray
        return resultsArray

    # If we are using hourly method
    if(method == 'hourly'):
        for m in measurements:
            # Now we put the measurement into the correct place in the results array
            addToResultsArray(float(m[3]), float(m[5]))
        return returnData()
    # If we are using daily method
    if(method == 'daily'):
        # We agregate hourly values for each day
        dailyAgregate = 0
        dailyRadiationAgragate = 0
        for m in measurements:
            # Add the temperature to the daily agregate
            dailyAgregate = dailyAgregate + float(m[3])
            # Add the radiation to the daily agregate
            dailyRadiationAgragate = dailyRadiationAgragate + float(m[4])
            # If we have reached the last hour
            if(float(m[2]) == 23):
                # Get the daily average temperature
                dailyAgregate /= 24
                # Get the daily average radiation
                dailyRadiationAgragate /= 24
                # Add a value to the results
                addToResultsArray(dailyAgregate, dailyRadiationAgragate)
                # Reset daily agregate
                dailyAgregate = 0
                dailyRadiationAgragate = 0
        # We have finished the for loop
        return returnData()
