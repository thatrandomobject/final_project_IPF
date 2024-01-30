import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import configparser

# visual aid for DataFrames
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

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
df['athlete_name'] = df['athlete_name'].str.split(' #').str[0]
df['age'] = pd.to_numeric(df['age'].str.replace('~', ''))
df['weight'] = pd.to_numeric(df['weight'])
df['squat'] = pd.to_numeric(df['squat'])
df['bench_press'] = pd.to_numeric(df['bench_press'])
df['deadlift'] = pd.to_numeric(df['deadlift'])
df['total'] = pd.to_numeric(df['total'])
df['glp_score'] = pd.to_numeric(df['glp_score'])
df['home'] = df['home'].str.split('-').str[0]
df['relative_strength'] = df['total']/df['weight']
df['longitude'] = df['home'].map(longitude, None)
df['latitude'] = df['home'].map(latitude, None)
df['age_group'] = df['age'].apply(age_group)

# CHART FUNCTIONS

# a function that draws 4 charts, 2 for male and 2 for female stats

def total_rs_gender(start_date, end_date, df):
    df = df[(df['event_date'] < f'{end_date}')&(df['event_date'] > f'{start_date}')]
    df_male = df[df['sex'] == 'M']
    average_total_male = df_male.groupby(['year'])['total'].mean()
    average_rs_male = df_male.groupby(['year'])['relative_strength'].mean()
    df_female = df[df['sex'] == 'F']
    average_total_female = df_female.groupby(['year'])['total'].mean()
    average_rs_female = df_female.groupby(['year'])['relative_strength'].mean()
    plt.figure(figsize=(8, 8))
    plt.subplot(2, 2, 1)
    average_rs_male.plot(kind='line')
    plt.ylim(4, 7)
    plt.xticks(rotation=0)
    plt.title('Average Male RS by Year')
    plt.ylabel('Ratio of Total to athlete Weight')
    plt.xlabel('Year')
    plt.subplot(2, 2, 2)
    average_rs_female.plot(kind='line')
    plt.ylim(4, 7)
    plt.xticks(rotation=0)
    plt.ylabel('Ratio of Total to athlete Weight')
    plt.title('Average Female RS by Year')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.subplot(2, 2, 3)
    average_total_male.plot(kind='bar')
    plt.ylim(0, 650)
    plt.xticks(rotation=0)
    plt.title('Average Male Total by Year')
    plt.ylabel('kg, total')
    plt.xlabel('Year')
    plt.subplot(2, 2, 4)
    average_total_female.plot(kind='bar')
    plt.ylim(0, 650)
    plt.xticks(rotation=0)
    plt.title('Average Female Total by Year')
    plt.ylabel('kg, total')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.show()


# total_rs_gender('2018-01-01', '2024-01-01', df)

# athlete count change by year seaborn barplot
def athlete_count_year(start_year, end_year, df):
    df = df[(df['year'] < end_year) & (df['year'] >= start_year)]
    athlete_count_by_year = df.groupby(['year'])['athlete_name'].count()
    plt.figure(figsize=(8, 8))
    sns.barplot(athlete_count_by_year)
    plt.title('Athlete Count by Year')
    plt.xlabel('Year')
    plt.ylabel('Athlete Count')
    plt.tight_layout()
    plt.show()


# athlete_count_year(2018, 2024, df)

# athlete count by home over years plotly time period 2018-2024
def athlete_count_country(start_year, end_year, df):
    df = df[(df['year'] < end_year)&(df['year'] >= start_year)]
    home_athlete_count = df.groupby(['home', 'longitude', 'latitude', 'year'])['athlete_name'].count()
    df_home_athlete_count = home_athlete_count.to_frame().reset_index().rename(columns={
        'home': 'Country',
        'longitude': 'Lon',
        'latitude': 'Lat',
        'year': 'Year',
        'athlete_name': 'Athlete Count'})
    fig = px.scatter_geo(df_home_athlete_count, lat='Lat', lon='Lon', color="Country",
                         size="Athlete Count", size_max=70,
                         animation_frame="Year",
                         projection="natural earth", title='Athlete Count by Country')
    fig.show()


# athlete_count_country(2018, 2024,df)

# top 5 strongest countries in year X by total
def top5_strongest_countries(year):
    strongest_countries = df[df['year'] == year].groupby('home')['total'].max().sort_values(ascending=False).head(5).reset_index()
    plt.figure(figsize=(8, 8))
    fig = sns.barplot(data=strongest_countries, x='home', y='total', hue='home')
    plt.title(f'Top 5 Countries by Total in {year}')
    plt.xlabel('Country')
    plt.ylabel('kg, Total')
    plt.tight_layout()
    for i in fig.containers:
        fig.bar_label(i)
    plt.show()


# top5_strongest_countries(2023)

# average age by gender by years

def average_age_by_year_gender(start_year, end_year, df):
    df = df[(df['year'] < end_year) & (df['year'] >= start_year) & (df['sex'] != 'Mx')]
    # df_male = df[df['sex'] == 'M']
    # df_female = df[df['sex'] == 'F']
    # grouped_df_m = df_male.groupby(['sex', 'year'])['age'].mean().reset_index()
    # grouped_df_f = df_female.groupby(['sex', 'year'])['age'].mean().reset_index()
    # grouped_df_m.plot(kind='line')
    plt.figure(figsize=(8, 8))
    sns.barplot(df, x='year', y='age', hue='sex')
    plt.title('Average Age of Athletes by Year')
    plt.legend(title='Gender')
    plt.xlabel('Year')
    plt.ylabel('Age')
    plt.show()

# average_age_by_year_gender(2018, 2024, df)

# average strength by age category bench, squat, deadlift


def average_strength_age_group(year, df):
    df = df[df['year'] == year]
    grouped_df = df.groupby('age_group')[['squat', 'bench_press', 'deadlift']].mean()
    plt.figure(figsize=(8, 8))
    plt.subplot(3, 1, 1)
    sns.barplot(grouped_df, x='age_group', y='squat', hue='age_group')
    plt.title(f'Average Squat for each Age Group in year {year}')
    plt.xlabel('Age group')
    plt.ylabel('kg, Strength')
    plt.subplot(3, 1, 2)
    sns.barplot(grouped_df, x='age_group', y='bench_press', hue='age_group')
    plt.title(f'Average Bench Press for each Age Group in year {year}')
    plt.xlabel('Age group')
    plt.ylabel('kg, Strength')
    plt.subplot(3, 1, 3)
    sns.barplot(grouped_df, x='age_group', y='deadlift', hue='age_group')
    plt.title(f'Average Deadlift for each Age Group in year {year}')
    plt.xlabel('Age group')
    plt.ylabel('kg, Strength')
    plt.tight_layout()
    plt.show()

# average_strength_age_group(2023, df)


