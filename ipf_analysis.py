import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import configparser
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# visual aid for DataFrames
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)
# removes error message, we are not sure if this affects our case as explained in pandas.pydata.org documentation
pd.options.mode.copy_on_write = True

# connection to postgreSQL
config = configparser.ConfigParser()
config.read('config.ini')
host = config['database']['host']
password = config['database']['password']
port = config['database']['port']
database = config['database']['database']
user = config['database']['user']

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

sql_query = "SELECT * FROM open_ipf;"  # reading all the data from an SQL table

# additional data (coordinates for countries)
latitude = {
    'USA': 37.090240,
    'Russia': 61.524010,
    'England': 52.355518,
    'Netherlands': 52.132633,
    'Canada': 56.130367,
    'Australia': -24.7761086,
    'Germany': 51.1638175,
    'Poland': 52.215933,
    'Scotland': 56.7861112,
    'Italy': 42.6384261,
    'Belgium': 50.6402809,
    'France': 46.603354,
    'Ireland': 52.865196,
    'New Zealand': -41.5000831,
    'Finland': 63.2467777,
    'Singapore': 1.357107,
    'Brazil': -10.3333333,
    'Ukraine': 49.4871968,
    'Norway': 61.1529386,
    'Czechia ': 49.7439047,
    'Japan': 36.5748441,
    'India': 22.3511148,
    'Sweden': 59.6749712,
    'Spain': 39.3260685,
    'South Africa': -28.8166236,
    'Argentina': -34.9964963,
    'Hungary': 47.1817585,
    'UK': 54.7023545,
    'Croatia': 45.3658443,
    'Serbia': 44.1534121,
    'Denmark': 55.670249,
    'Lithuania': 55.3500003
}
longitude = {
    'USA': -95.712891,
    'Russia': 105.318756,
    'England': -1.174320,
    'Netherlands': 5.291266,
    'Canada': -106.346771,
    'Australia': 134.755,
    'Germany': 10.4478313,
    'Poland': 19.134422,
    'Scotland': -4.1140518,
    'Italy': 12.674297,
    'Belgium': 4.6667145,
    'France': 1.8883335,
    'Ireland': -7.9794599,
    'New Zealand': 172.8344077,
    'Finland': 25.9209164,
    'Singapore': 103.8194992,
    'Brazil': -53.2,
    'Ukraine': 31.2718321,
    'Norway': 8.7876653,
    'Czechia': 15.3381061,
    'Japan': 139.2394179,
    'India': 78.6677428,
    'Sweden': 14.5208584,
    'Spain': -4.8379791,
    'South Africa': 24.991639,
    'Argentina': -64.9672817,
    'Hungary': 19.5060937,
    'UK': -3.2765753,
    'Croatia': 15.6575209,
    'Serbia': 20.55144,
    'Denmark': 10.3333283,
    'Lithuania': 23.7499997
}

# reading data from sql and defining a data frame with dropped Null values
df = pd.read_sql_query(sql_query, engine)
df = df.dropna()

# data clean-up, mapping and other data preparation


def age_group(age):
    if age <= 18:
        return '01 Sub-Junior'
    elif age < 25:
        return '02 Junior'
    elif age < 35:
        return '03 Senior'
    else:
        return '04 Master'


df['event_date'] = pd.to_datetime(df['event_date'])
df['year'] = df['event_date'].dt.year.astype(int)
df['month'] = df['event_date'].dt.month.astype(int)
df['athlete_name'] = df['athlete_name'].str.split(' #').str[0]
df['age'] = pd.to_numeric(df['age'].str.replace('~', ''))
df['weight'] = pd.to_numeric(df['weight'])
df['squat'] = pd.to_numeric(df['squat'])
df['bench_press'] = pd.to_numeric(df['bench_press'])
df['deadlift'] = pd.to_numeric(df['deadlift'])
df['total'] = pd.to_numeric(df['total'])
df['glp_score'] = pd.to_numeric(df['glp_score'])
df['home'] = df['home'].str.split('-').str[0]
df['relative_strength'] = df['total']/df['weight']  # calculation of relative strength
df['longitude'] = df['home'].map(longitude, None)  # mapping of longitude to home
df['latitude'] = df['home'].map(latitude, None)  # mapping of latitude to home
df['age_group'] = df['age'].apply(age_group)  # applying age_group function

# CHART FUNCTIONS

# a function that draws 4 charts, 2 for male and 2 for female stats


def total_rs_gender(start_date, end_date):
    # set function arguments as variables
    start_date = start_date
    end_date = end_date
    # apply time filter to main data frame
    time_filtered_df = df[(df['event_date'] < f'{end_date}') & (df['event_date'] > f'{start_date}')]
    # apply gender filter
    df_male = time_filtered_df[time_filtered_df['sex'] == 'M']
    # groupby and calculate averages
    average_total_male = df_male.groupby(['year'])['total'].mean()
    average_rs_male = df_male.groupby(['year'])['relative_strength'].mean()
    df_female = time_filtered_df[time_filtered_df['sex'] == 'F']
    average_total_female = df_female.groupby(['year'])['total'].mean()
    average_rs_female = df_female.groupby(['year'])['relative_strength'].mean()
    # setting up min and max limits for y-axis
    max_male_total = average_total_male.max()
    max_female_total = average_total_female.max()
    max_rs_male = average_rs_male.max()
    min_rs_male = average_rs_male.min()
    max_rs_female = average_rs_female.max()
    min_rs_female = average_rs_female.min()
    if max_male_total > max_female_total:
        bar_upper_limit = max_male_total
    else:
        bar_upper_limit = max_female_total
    if max_rs_male > max_rs_female:
        line_upper_limit = max_rs_male
    else:
        line_upper_limit = max_rs_female
    if min_rs_female < min_rs_male:
        line_lower_limit = min_rs_female
    else:
        line_lower_limit = min_rs_male
    # set figure size
    plt.figure(figsize=(8, 8))
    # define subplots
    plt.subplot(2, 2, 1)
    # define type of plot
    average_rs_male.plot(kind='line')
    # set limits to y-axis
    plt.ylim(line_lower_limit * 0.8, line_upper_limit * 1.2)
    # set formatting of text of x-axis
    plt.xticks(rotation=0)
    # set title of chart
    plt.title('Average Male RS by Year')
    # set title of y-axis
    plt.ylabel('Ratio of Total to Athlete Weight')
    # set title of x-axis
    plt.xlabel('Year')
    # do the same for other plots
    plt.subplot(2, 2, 2)
    average_rs_female.plot(kind='line')
    plt.ylim(line_lower_limit * 0.8, line_upper_limit * 1.2)
    plt.xticks(rotation=0)
    plt.ylabel('Ratio of Total to Athlete Weight')
    plt.title('Average Female RS by Year')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.subplot(2, 2, 3)
    average_total_male.plot(kind='bar')
    plt.ylim(0, bar_upper_limit * 1.1)
    plt.xticks(rotation=0)
    plt.title('Average Male Total by Year')
    plt.ylabel('kg, Total')
    plt.xlabel('Year')
    plt.subplot(2, 2, 4)
    average_total_female.plot(kind='bar')
    plt.ylim(0, bar_upper_limit * 1.1)
    plt.xticks(rotation=0)
    plt.title('Average Female Total by Year')
    plt.ylabel('kg, Total')
    plt.xlabel('Year')
    # removes overlapping and others issues with alignment
    plt.tight_layout()
    # show chart
    plt.show()


# total_rs_gender('2018-01-01', '2024-01-01')

# athlete count change by year seaborn barplot
def athlete_count_year(start_year, end_year):
    # filter time
    start_year = start_year
    end_year = end_year
    df_time_filtered = df[(df['year'] < end_year) & (df['year'] >= start_year)]
    # value_counts() is used to find the repeating names and index reset is done convert series to dataframe so that
    # we could group it again
    grouped_athlete_count_by_year = df_time_filtered.groupby('year')['athlete_name'].value_counts().reset_index()
    # counting unique athletes
    athlete_count_by_year = grouped_athlete_count_by_year.groupby('year')['athlete_name'].count()
    # setting figure size
    plt.figure(figsize=(8, 8))
    # using seaborn to plot the data as a bar plot
    sns.barplot(athlete_count_by_year)
    plt.title('Athlete Count by Year')
    plt.xlabel('Year')
    plt.ylabel('Athlete Count')
    plt.tight_layout()
    plt.show()


# athlete_count_year(2018, 2024)

# athlete count by home over years plotly time period 2018-2024
def athlete_count_country(start_year, end_year):
    df_year_filtered = df[(df['year'] < end_year) & (df['year'] >= start_year)]
    # grouping the data by country, the coordinates and year
    home_athlete_count = df_year_filtered.groupby(['home', 'longitude', 'latitude', 'year'])['athlete_name'].count()
    # resetting indexes and renaming columns for use in plotly scatter_geo chart
    df_home_athlete_count = home_athlete_count.to_frame().reset_index().rename(columns={
        'home': 'Country',
        'longitude': 'Lon',
        'latitude': 'Lat',
        'year': 'Year',
        'athlete_name': 'Athlete Count'})
    # defining plotly figure
    print(df_home_athlete_count)
    fig = px.scatter_geo(df_home_athlete_count, lat='Lat', lon='Lon', color="Country",
                         size="Athlete Count", size_max=60,
                         animation_frame="Year",
                         projection="natural earth", title='Athlete Count by Country')
    fig.show()


# athlete_count_country(2018, 2024)

# top 5 strongest countries in year X by total
def top5_strongest_countries(year):
    year = year
    # finding the top 5 countries by total for the entered 'year'
    strongest_countries = df[df['year'] == year].groupby('home')['total'].max().sort_values(ascending=False).head(5).reset_index()
    plt.figure(figsize=(8, 8))
    fig = sns.barplot(data=strongest_countries, x='home', y='total', hue='home')
    plt.title(f'Top 5 Countries by Total in {year}')
    plt.xlabel('Country')
    plt.ylabel('kg, Total')
    plt.tight_layout()
    # adding in values at the top of bars
    for i in fig.containers:
        fig.bar_label(i)
    plt.show()


# top5_strongest_countries(2023)

# average age by gender by years

def average_age_by_year_gender(start_year, end_year):
    df_filtered = df[(df['year'] < end_year) & (df['year'] >= start_year) & (df['sex'] != 'Mx')]
    plt.figure(figsize=(8, 8))
    sns.barplot(df_filtered, x='year', y='age', hue='sex')
    plt.title('Average Age of Athletes by Year')
    plt.legend(title='Gender')
    plt.xlabel('Year')
    plt.ylabel('Age')
    plt.tight_layout()
    plt.show()


# average_age_by_year_gender(2018, 2024)

# average strength by age category bench, squat, deadlift

def average_strength_age_group(year):
    df_year = df[df['year'] == year]
    grouped_df = df_year.groupby('age_group')[['squat', 'bench_press', 'deadlift']].mean()
    plt.figure(figsize=(8, 8))
    plt.subplot(3, 1, 1)
    sns.barplot(grouped_df, x='age_group', y='squat', hue='age_group')
    plt.title(f'Average Squat for Each Age Group in Year {year}')
    plt.xlabel('Age group')
    plt.ylabel('kg, Strength')
    plt.subplot(3, 1, 2)
    sns.barplot(grouped_df, x='age_group', y='bench_press', hue='age_group')
    plt.title(f'Average Bench Press for Each Age Group in Year {year}')
    plt.xlabel('Age group')
    plt.ylabel('kg, Strength')
    plt.subplot(3, 1, 3)
    sns.barplot(grouped_df, x='age_group', y='deadlift', hue='age_group')
    plt.title(f'Average Deadlift for Each Age Group in Year {year}')
    plt.xlabel('Age group')
    plt.ylabel('kg, Strength')
    plt.tight_layout()
    plt.show()

# average_strength_age_group(2023)


def relative_strength_regression(date_start, date_end):
    date_start = date_start
    date_end = date_end
    # filter and sort in ascending order of events
    filtered_df = df[(df['event_date'] >= date_start) & (df['event_date'] < date_end)
                     & (df['equip'] == 'Classic') & (df['sex'] != 'Mx')].sort_values('event_date')
    # group dataframe and reset_index to convert from series to dataframe
    grouped_df = filtered_df.groupby(['sex', 'year', 'month'])['relative_strength'].mean().reset_index()
    gender_list = ['F', 'M']
    # create charts for both genders
    for gender in gender_list:
        # filter to gender data
        gender_df = grouped_df[grouped_df['sex'] == gender]
        # set length of time into the future for prediction
        future_months = 12
        # create a time variable for splitting. I believe it is possible to do this with time variables,
        # but need to study it more
        gender_df['Month_index'] = range(1, len(gender_df)+1)
        # creating a Date column in the df in order to have a column with the same name and consistent dates
        gender_df['Date'] = pd.to_datetime(gender_df[['year', 'month']].assign(DAY=1))
        # get the latest month in the index
        last_month_index = max(gender_df['Month_index'])
        # create a dataframe for future prediction which follows after actual data
        future_df_g = pd.DataFrame({'Month_index': np.arange(last_month_index+1, last_month_index+future_months+1)})
        # set a start date from which to predict
        start_date = pd.to_datetime(date_end)
        # generate a date column for future_df_g
        future_df_g['Date'] = pd.date_range(start=start_date, periods=12, freq='MS')
        # concatenate old and new dataframes
        extended_df_f = pd.concat([gender_df, future_df_g], ignore_index=True)
        # setting the independent and dependent variables
        X = gender_df[['Month_index']]
        y = gender_df['relative_strength']
        # define the extended X axis
        X_extended = extended_df_f[['Month_index']]
        # creating training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        # choosing the model
        model = LinearRegression()
        # training the model
        model.fit(X_train, y_train)
        # testing the prediction model by checking the mean squared error
        y_predict = model.predict(X_test)
        mse = mean_squared_error(y_test, y_predict)
        print(f'Mean squared error is: {mse}')
        # extended data based on the training model
        y_future_predict = model.predict(X_extended)
        plt.figure(figsize=(8, 8))
        # plot actual data for gender relative strength
        plt.plot(gender_df['Date'], gender_df['relative_strength'],
                 label=f'Actual Data of Average Relative Strength, {gender}')
        # plot prediction for 12months of relative data
        plt.plot(future_df_g['Date'], y_future_predict[-future_months:],
                 linestyle='dotted', label=f'Predicted RS, {gender}')
        plt.title(f'Relative Strength Prediction for Classic Athletes Over Time, {gender}')
        plt.xlabel('Time')
        plt.ylabel('kg, Relative Strength')
        plt.legend()
    plt.show()

# regression of unequiped/classic strength over years for bench, squat, deadlift


# relative_strength_regression('2018-01-01', '2024-01-01')



