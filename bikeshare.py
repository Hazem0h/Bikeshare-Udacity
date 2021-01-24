import time
import pandas as pd
import numpy as np

# A dict for the city names. Could be an ordinary list though
CITY_NAMES = { 1: 'chicago.csv',
              2: 'new_york_city.csv',
              3: 'washington.csv' }

# Filter types 
NO_FILTER = "No filter"
FILTER_TYPE_BOTH = "DAY and MONTH"
FILTER_TYPE_DAY = "DAY"
FILTER_TYPE_MONTH = "MONTH"
chosen_filter = ""

# An array for the days
DAYS = [NO_FILTER,  "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# An array for the months
MONTHS = [NO_FILTER, "January", "February", "March", "April", "May", "June"]

# Encoding the city type (to know if we have extended columns or not)
CITY_TYPE_EXTENDED = 0
CITY_TYPE_SHORT = 1
city_type = -1


def choose_file():
    """
    Takes input from the user for the specified city and returns a Pandas dataframe of the corresponding csv file

    No arguments

    Returns:
        city_data : Pandas dataframe
    """
    print("Please enter the city number you are interested in")
    city_input = input("Enter \n1 for Chicago\n2 for New York City \n3 for Washington\n")

    while(True):

        try:
            city_num = int(city_input)
            if(city_num in range(1,4)):
                break
            else:
                print("Number out of range. You entered {}. \nplease Enter either 1 or 2 or 3".format(city_num))
        except ValueError:
            print("Wrong input. You entered {} \nPlease enter a number 1 or 2 or 3".format(city_input))

        city_input = input("Enter \n1 for Chicago\n2 for New York City \n3 for Washington\n")

    print("Great! You chose {}".format((CITY_NAMES[city_num]).replace("_", " ")[0:-4]))
    print("-"*40)

    # Don't forget to set the city type, will be used in user statistics
    global city_type
    if city_num == 3:
        # If the chosen city is Washington
        city_type = CITY_TYPE_SHORT
    else:
        city_type = CITY_TYPE_EXTENDED
    return pd.read_csv(CITY_NAMES[city_num])

def choose_time_filter():
    """Takes user input to filter data according to day and/or month

    Arguments: 
        No arguments

    Returns:
        month :(int)
        day: (int)
    """
   
    while(True):
        month_str = input("Do you want to filter the data by month? \nEnter an integer value for month (1 for January until 6 for June, 0 for no filter)\n")
        try:
            month = int(month_str)
            if month in range(0,7):
                break
            else:
                print("Number {} is out of range. The number should be between 0 and 6 inclusive".format(month))
        except ValueError:
            print("Couldn't parse the input {} \nPlease only enter a numeric value".format(month_str))

    while(True):
        day_str = input("Do you want to filter the data by day? \nEnter an integer value for the day (1 for Monday, 2 for Tuesday..., 0 for no filter)\n")
        try:
            day = int(day_str)
            if day in range(0,8):
                break
            else:
                print("Number {} is out of range. The number should be between 0 and 7 inclusive".format(day))
        except ValueError:
            print("Couldn't parse the input {} \nPlease only enter a numeric value".format(day_str))
    
    return month, day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze, and loads the corresponding data

    Returns:
        (Pandas dataframe) city_data - dataframe of the read csv file
        (int) month - number of the month to filter by, or 0 for "no filter" to apply no month filter
        (int) day - number of the day of week to filter by, or 0 for "no filter" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get the desired city data from the user
    # I will resort to integer input because I think it is less error prone with respect to a typical end user
    # Entering a number is simpler than entering whole words

    city_data = choose_file()
    
    # get user input for month (all, january, february, ... , june) and\or day (Sunday, Monday, Tuesday,..., )
    month, day = choose_time_filter()

    month_filter = MONTHS[month]
    day_filter = DAYS[day]

    global chosen_filter
    if(month_filter != NO_FILTER and day_filter != NO_FILTER):

        chosen_filter = FILTER_TYPE_BOTH
        print("Data will be filtered to {}s of {}".format(day_filter, month_filter))

    elif(month_filter == NO_FILTER and day_filter == NO_FILTER):

        chosen_filter = NO_FILTER
        print("No filter will be applied to the data")

    elif(month_filter != NO_FILTER):

        chosen_filter = FILTER_TYPE_MONTH
        print("Data will filtered to the month of {}".format(month_filter))
    else:
        
        chosen_filter = FILTER_TYPE_DAY
        print("Data will be filtered to {}s".format(day_filter))

    print('-'*40)
    return city_data, month, day


def load_data(city_data, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (Pandas dataframe) city_data - name of the city to analyze
        (int) month - number of the month to filter by, or 0 for "no_filter" to apply no month filter
        (int) day - number of the day of week to filter by, or 0 for "no_filter" to apply no day filter
    Returns:
        data_filtered - Pandas DataFrame containing city data filtered by month and/or day, if any filter exists
    """
    # First, change the Start Time and End Time columns to datetime datatype
    # This will make it easy to perform any type of logic on "time realted statistics"
    city_data["Start Time"] = pd.to_datetime(city_data["Start Time"])
    city_data["End Time"] = pd.to_datetime(city_data["End Time"])

    # Initialize the filtered dataframe to the original
    data_filtered = city_data

    #Perform filtering
    if month != 0:
        # Filter by month
        data_filtered = data_filtered[data_filtered["Start Time"].dt.month == month]
    
    if day != 0:
        # Filter by day
        # Here we subtract by one because the data entered by the user starts with 1 for Monday
        # Whereas pandas dayofweek starts at 0 for Monday
        data_filtered = data_filtered[data_filtered["Start Time"].dt.dayofweek == (day-1)]
    
    return data_filtered


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print("Filter Type: {}".format(chosen_filter))
    start_time = time.time()

    # display the most common month
    if chosen_filter == NO_FILTER or chosen_filter == FILTER_TYPE_DAY:
        # Naturally, we will only print the most common month if we haven't filtered the data by month
        # There is a variable to keep track of that, which is "chosen_filter" and it only takes a value from 
        # a set of predefined constants
        most_common_month_index = df["Start Time"].dt.month.mode()[0]
        print("The most common month is {}".format(MONTHS[most_common_month_index]))

    # display the most common day of week
    if chosen_filter == NO_FILTER or chosen_filter == FILTER_TYPE_MONTH:
        # Same as for months. Will only type the most common day if it were not filtered per day
        most_common_day_index = df["Start Time"].dt.dayofweek.mode()[0]
        print("The most common day is {}".format(DAYS[most_common_day_index +1 ]))  #+1 because dayofweek starts with 0

    # display the most common start hour
    most_common_start_hour = df["Start Time"].dt.hour.mode()[0]
    print("The most common start hour is {}".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print("Filter Type: {}".format(chosen_filter))
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print("The most common start station is {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("The most common end station is {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    # First we will create a new  column to include the combination of start and end stations, then,
    # We will get the most frequent trip by getting the mode
    df["Trip"] = df["Start Station"] + "-" + df["End Station"] 
    most_common_trip = (df["Trip"].mode()[0]).split("-") # will split the start and the end stations
    print("The most common trip path is from {} to {}".format(most_common_trip[0], most_common_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print("Filter Type: {}".format(chosen_filter))
    start_time = time.time()

    # display total travel time
    total_duration = df["Trip Duration"].sum()
    hours =  total_duration // 3600
    minutes = (total_duration - hours * 3600)//60
    seconds = (total_duration - hours * 3600 - minutes * 60)

    print("Total travel time is {} hours: {} minutes: {} seconds".format(hours, minutes, seconds))

    # display mean travel time
    mean_duration = df["Trip Duration"].mean()
    hours =  mean_duration // 3600
    minutes = (mean_duration - hours * 3600)//60
    seconds = (mean_duration - hours * 3600 - minutes * 60)

    print("Average travel time is {} hours: {} minutes: {} seconds".format(hours, minutes, seconds))

    #--------------------------------------------------------------
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print("Filter type: {}".format(chosen_filter))
    start_time = time.time()

    # Display counts of user types
    print("The user types are: ")
    user_types = df["User Type"]
    print(user_types.value_counts().to_string())
    print("*"*20)

    # The gender and birth year data will only be available for chicago and New York
    # We keep track of it using the city_type global variable
    if city_type == CITY_TYPE_EXTENDED:
        # Display counts of gender
        print("Gender data:")
        print(df["Gender"].value_counts().to_string())
        print("*"*20)

        # Display earliest, most recent, and most common year of birth
        print("Birth year data:")
        earliest_birthyear = df["Birth Year"].min()
        latest_birthyear = df["Birth Year"].max()
        most_common_birthyear = df["Birth Year"].mode()[0]
        print("Most common birth year: {}".format(most_common_birthyear))
        print("Latest birth year: {}".format(latest_birthyear))
        print("Earliest birth year: {}".format(earliest_birthyear))


        print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)

def disp_raw_data(df):
    df.drop(["Unnamed: 0"], axis = "columns", inplace = True)
    n = 0
    #df.reset_index(drop=True, inplace = True)
    raw_data_flag = input("\nDo you want to display raw data? [y/n]\n")
    while(len(raw_data_flag) > 0 and  raw_data_flag.lower()[0] == "y" and n <= df.size):
        ending_index = min(n+5, df.size)
        print(df.iloc[n:ending_index])
        n += 5
        raw_data_flag = input("\nDo you want to display raw data? [y/n]\n")


def main():
    while(True):
        # extracting the data
        city_data, month, day = get_filters()
        filtered = load_data(city_data, month, day)
        filtered_copy = filtered.copy()

        # Displaying description statistics
        time_stats(filtered)
        station_stats(filtered)
        trip_duration_stats(filtered)
        user_stats(filtered)

        # Displaying raw data
        disp_raw_data(filtered_copy)

        restart = input('\nWould you like to restart? [y/n]\n')
        if restart.lower()[0] != "y":
            break


if __name__ == "__main__":
	main()
    