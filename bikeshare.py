# This is a project from Udacity's Data science nanodegree program

# Sources consulted during the development of this solution are listed below

# https://towardsdatascience.com/a-quick-introduction-to-the-pandas-python-library-f1b678f34673

# https://www.kaggle.com/code/grigoryminch/case-study-how-does-a-bike-share-navigate-speedy/notebook

# https://stackoverflow.com/questions/53086118/python-for-dummies-using-the-bakeshare-data


import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Requests that the user(s) should specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hi! Let\'s explore some bikeshare data! Ready?')
    print()
    # We need to get user input for city (chicago, new york city, washington) We use a while loop to handle some of the invalid inputs
    while True:
        city = input(
            'We have data from Chicago, New York City and Washington cities, choose which to explore: \n\n').lower()
        print()
        if city in CITY_DATA:
            break
        print('Invalid data input!\n')

    # Also, get user input for month (all, january, february, ... , june)

    while True:
        month_name = input("Type 'all' for no month filter or january, february, ... , june for monthly data: \n\n")
        month = month_name.lower()
        # A month has been chosen, so we analyze it
        if month in months:
            break
        # We were unable to get a right month name for analysis, so the loop continues.
        print("Invalid data input!\n\n")

    # Request the day of the week (all, monday, tuesday, ... sunday)
    while True:
        day_name = input("\nSelect sunday, monday, ..., saturday to see weekday results or all for no filter.\n\n")
        day = day_name.lower()
        if day in days:
            break
        # Since the input was wrong, the loop continues till the right day is selected
        print("Invalid input")

    print('-' * 40)
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
    # Load the data file into pandas dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create a new column by extracting month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # We will use index of the months list to get the corresponding int
        month = months.index(month)

        # Create a new dataframe front the month filter the user applied
        df = df.loc[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # create a new dataframe from day of week filter applied by the user
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('ALERT!!!\n The returned statistics below are based on the city, month and day filter you earlier applied!\n')

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    month_title = months[common_month].title()
    print('The most common month is: {}'.format(month_title))
    print()

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is: {}'.format(common_day))
    print()

    # Display the most common start hour
    common_start_hour = str(df['hour'].mode()[0])
    print('The most common start hour is: {}'.format(common_start_hour))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most used Start Station is: {}'.format(common_start_station))
    print()

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most used End Station is: {}'.format(common_end_station))
    print()

    # Display most frequent combination of start and end station trip
    frequent_combination = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print('The most frequent combination of Start and End Stations is: {}'.format(frequent_combination))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print()
    start_time = time.time()

    # The total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: {}'.format(total_travel_time))
    print()

    # Show the average travel time
    average_travel_time = df['Trip Duration'].mean()
    print('The average time travelled is: {}'.format(average_travel_time))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The count of each user type is: {}'.format(str(user_types)))
    print('-' * 40)


def birth_year_stats(df):
    """ Display statistics on the gender & birth year of the bikeshare users."""
    start_time = time.time()
    if 'Birth Year' in df.columns:
        print('\nCalculating User Gender & Birth Year of the city...\n')

        # Display gender counts
        gender = df['Gender'].value_counts()
        print('The user gender count is: {} \n'.format(str(gender)))
        print()

        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        print('Our oldest riders were born in: {}\n'.format(earliest_birth))
        print()

        most_recent_birth = df['Birth Year'].max()
        print('Our youngest riders were born in: {}\n'.format(most_recent_birth))
        print()

        most_common_birth = df['Birth Year'].mode()[0]
        print('The most popular riders were born in: {}\n'.format(most_common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """This block of codes displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame that contains city data filtered by month and day
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(df.head())
    n = 0
    while True:
        raw_data = input("\nType 'yes' to display 5 rows of the raw data, or 'no' to bypass.\n")
        if raw_data.lower() == 'yes':
            n = n + 5
            print(df.iloc[n - 5:n, :])
        elif raw_data.lower() == 'no':
            break
        else:
            print('Invalid input')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        birth_year_stats(df)
        x = 0
        while True:
            raw_data = input("\nType 'yes' to display 5 rows of the raw data or 'no' to bypass.\n")
            if raw_data.lower() == 'yes':
                x = x + 5
                print(df.iloc[x - 5:x, :])
            elif raw_data.lower() == 'no':
                break
            else:
                print('Invalid input')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
