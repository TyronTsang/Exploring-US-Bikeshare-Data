#Importing the libraries  add bikesahre_2.py

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    global input_month
    global input_day

    month = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    """
    Asks user to specify a city, month, and day to analyze the data needed for inputting 

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ['chicago', 'washington', 'new york city']
    while True:
        input_city = input('Would you like to select chicago, new york city or washington?').lower()
        if input_city not in city:
            print('You might have misplet the city or the city doesnt exist! Please try again!', end='')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        input_month = input('Please select a month or all:').lower()
        if input_month not in month:
            print('You might have mispelt the month, please try again!', end='')
            continue
        else:
            break


    while True:
        input_day = input('Please select a day of the week or all:').lower()
        if input_day not in day:
            print('You might have misplet the day, please try again!')
            continue
        else:
            break


    print('-'*40)
    return input_city, input_month, input_day


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

    #load data into dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert start time and end time into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #extract month and day of the week from Start time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_the_week'] = df['Start Time'].dt.weekday_name
    df['Start hour'] = df['Start Time'].dt.hour

    #filter by month if applicable
    if month != 'all':
        #use the index of the months list to get corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day of the week if applicable
    if day != 'all':
        #filter by the day of the week to create a new dataframe
        df = df[df['day_of_the_week'] == day.title()]
        print('You have selected the following:\nCity: {}\nMonth: {}\nDay: {}'.format(city,month,day))
    return df


def time_statistics(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)


    # display the most common day of week
    common_dow = df['day_of_the_week'].mode()[0]
    print('Most common day of the week:',common_dow)


    # display the most common start hour
    common_hour = df['Start hour'].mode()[0]
    print('Most common hour:',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_statistics(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df.loc[:,'Start Station'].mode()[0]
    print('Most common start station is:', common_start_station)

    # display most commonly used end station
    common_end_station = df.loc[:,'End Station'].mode()[0]
    print('Most common end station is:', common_end_station)

    # display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of start and end station trips:',start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df["Trip Duration"] = df["End Time"] - df["Start Time"]
    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total travel time for your trip:', total_duration)
    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('The average time for your trip:',mean_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print('Gender count:', user_gender)
    else:
        print('There is no gender column')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_dob = df['Birth Year'].min()
        print('Earliest date of birth:', earliest_dob)
    else:
        print('There is no date of birth column')

    if 'Birth Year' in df.columns:
        recent_dob = df['Birth Year'].max()
        print('Recent date of birth:', recent_dob)
    else:
        print('There is no date of birth column')

    if 'Birth Year' in df.columns:
        common_dob = df['Birth Year'].mode()[0]
        print('Most common date of birth:', common_dob)
    else:
        print('There is no date of birth column')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
