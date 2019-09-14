import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
MONTH_DATA = {'1': 'all', '2': 'january', '3': 'february', '4': 'march', '5': 'april', '6': 'may', '7': 'june', '8': 'july',
               '9': 'august', '10': 'september', '11': 'october', '12': 'november', '13': 'december'}

DAY_DATA = {'1': 'all', '2': 'monday', '3': 'tuesday', '4': 'wednesday', '5': 'thursday', '6': 'friday',
            '7': 'saturday', '8': 'sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    isValid = False
    while not isValid:
        print("Available Cities \n 1 (All Cities) \n 2 (New York City) \n 3 (Chicago) \n 4 (Washington) \n")
        map_city = input('What city (or all) would you like to observe Bike Sharing Data? Choose a number! ')
        if map_city == '1':
            city = "all"
            isValid = True
        elif map_city == '2':
            city = "new york city"
            isValid = True
        elif map_city == '3':
            city = "chicago"
            isValid = True
        elif map_city == '4':
            city = "washington"
            isValid = True
        else:
            print('You have to choose between Chicago, New York City, Washington. Choose a number!\n ')
    # get user input for month (all, january, february, ... , june)
    isValid = False
    while not isValid:
        for key, value in MONTH_DATA.items():
            print("{} ({})".format(key, value.title()))

        map_month = input('What month of data would you like to see? Choose a number!\n ')
        if map_month in MONTH_DATA:
            month = MONTH_DATA[map_month]
            isValid = True
        else:
            print('You have to choose a valid month. Choose a number! ')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    isValid = False
    while not isValid:
        for key, value in DAY_DATA.items():
            print("{} ({})".format(key, value.title()))
        map_day = input('What day of the week would you like to see? Choose a number!\n ')
        if map_day in DAY_DATA:
            day = DAY_DATA[map_day]
            isValid = True
        else:
            print('You have to choose a valid day of the week. Choose a number!\n ')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city != "all":
        print("Loading Data... Please be patient :) ")
        df = pd.read_csv(CITY_DATA[city])
    else:
        print("Loading Data... Please be patient :) \n ")
        print("City Chosen: {}".format(city.title()))
        df = pd.concat(map(pd.read_csv, list(CITY_DATA.values())), sort=False)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.weekday_name

    if city == 'washington':
        df['Gender'] = 'Unknown'
        df['Birth Year'] = 2000

    if month != 'all':
        is_month = df['Month'] == month.title()

        if is_month.any():
            df = df[is_month]
        else:
            print("{} is not available in the data set \n".format(month.title()))
    if day != 'all':
        is_day = df['Day'] == day.title()

        if is_day.any():
            df = df[is_day]
        else:
            print("{} is not available in the data set \n".format(day.title()))

    print("Loading Basic Data about the city: {} \n".format(city.title()))
#     print(df.head(25))
    return df

def clean_data(df):
    """Clean up missing data and/or corrupted Data"""

    start_time = time.time()
    print("\nCleaning up Data. Please be patient...\n")
    missing_data = df.isnull().sum().sum()
    print("Currently a total of {} missing data values \n".format(missing_data))
    # replace and fill-in each column with the appropriate standard data point
    if missing_data != 0:
        df['Trip Duration'].fillna(df['Trip Duration'].mean(), inplace=True)
        df['User Type'].fillna('Dependent', inplace=True)
        df['Gender'].fillna('Unknown', inplace=True)
        df['Birth Year'].fillna(df['Birth Year'].mean(), inplace=True)
        missing_data_update = df.isnull().sum().sum()
        print("Post-Cleaning: Currently a total of {} missing data values \n".format(missing_data_update))
#         print(df.head(25))
    print("\n This took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()
    print('Most Popular Month: ', popular_month[0])

    # display the most common day of week
    popular_week = df['Day'].mode()
    print('Most Popular Day of the Week: ', popular_week[0])

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()
    print('Most Popular Hour: ', popular_hour[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()
    print('Most Popular Start Station: ', popular_start[0])

    # display most commonly used end station
    popular_end = df['End Station'].mode()
    print('Most Popular End Station: ', popular_end[0])

    # display most frequent combination of start station and end station trip
    df['Start End Combination'] = df['Start Station'] + ' TO ' + df['End Station']
    popular_combo = df['Start End Combination'].mode()
    print('Most Popular Start & End Combo: ', popular_combo[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_minutes = total_time / 60
    total_time_hours = total_time_minutes / 60
    total_time_days = total_time_hours / 24
    total_time_years = total_time_days / 365
    print('Total Travel Time in Seconds: ', total_time)
    print('Total Travel Time in Minutes: ', total_time_minutes)
    print('Total Travel Time in Hours: ', total_time_hours)
    print('Total Travel Time in Days: ', total_time_days)
    print('Total Travel Time in Years: ', total_time_years)

          # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time_minutes = mean_time / 60
    print('Total Avg Travel Time in Seconds: ', mean_time)
    print('Total Avg Travel Time in Minutes: ', mean_time_minutes)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    user_counts = user_type.tolist()
    user_values = user_type.keys().tolist()

    for value, count in zip(user_values, user_counts):
        print("{}: {}".format(value, count))

    # Display counts of gender
    if (city != 'washington'):
        gender = df['Gender'].value_counts()
        gender_values = gender.keys().tolist()
        gender_counts = gender.tolist()

        for value, count in zip(gender_values, gender_counts):
            print("{}: {}".format(value, count))

    # Display earliest, most recent, and most common year of birth
    if (city != 'washington'):
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()
        print('Earliest Year of Birth: ', int(earliest_year))
        print('Most Recent Year of Birth: ', int(most_recent_year))
        print('Most Common Year of Birth: ', int(common_year[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        clean_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
