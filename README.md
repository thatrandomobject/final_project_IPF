# INTERNATIONAL OPEN POWERLIFTING RATINGS ANALYSIS

## Details

## Created by: Linas Vaičiūnas and Rita Masionė

This is the final project by students for Vilnius Coding School.
Project theme: Sport Competition Analysis.

This project is designed to collect data (Web Scraping), analyse and visualize data for the sport of powerlifting competitions from various federations (IPF, LJTF and etc) in order to identify trends in the activities of the athletes grouped by gender, age, countries, and to perform comparative analysis over time. Chosen webpage contains data for 1973-2023. And all data was scraped for this project's purpose. Just the graphs represent the results of the last five years (2018-2023).
Python language in PyCharm environment, CSV files and Database (PostgreSQL) were used as tools.

## Libraries used:
+ selenium
+ psycopg2
+ webdriver_manager
+ configparser
+ pandas
+ numpy
+ sqlalchemy
+ matplotlib
+ seaborn
+ plotly.express
+ sklearn.model_selection
+ sklearn.linear_model
+ time

## ipf_scraper.py:
+ Piece of code which scrapes the website https://www.openipf.org/.
+ To fully scrape the website it took 62,863 seconds – this generated 165,386 rows of data. We wanted to fully scrape the website, since the sorting of the data in the website was not according to date and we wanted to have as much data from recent times as possible.

## ipf_analysis.py:
The file contains the connection to postgreSQL database in order to retrieve the data previously scraped by ipf_scraper.py using sqlalchemy library as well as configparser;
Using pandas a DataFrame is formed, Null values are dropped and further data ‘clean-up’, column creation, mapping of locations and age_groups is done;
The file contains 7 functions:
+ age_group(age) – a simple function used in creation of column of the same name in the DataFrame
+ total_rs_gender(start_date, end_date)
+ athlete_count_year(start_year, end_year)
+ athlete_count_country(start_year, end_year)
+ top5_strongest_countries(year)
+ average_age_by_year_gender(start_year, end_year)
+ average_strength_age_group(year)
+ relative_strength_regression(date_start, date_end)

## Linear graphs No. 1, No. 2, and bar graphs No. 3, No. 4:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/rs%20and%20total%20by%20gender.png)
## Linear graph No. 5:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/female%20rs%20projection.png)
## Linear graph No 6:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/male%20rs%20projection.png)
## Bar graph No. 7:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/athlete%20count%20by%20year.png)
## Map graph No. 8:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/athlete%20count%20by%20country.png)
## Bar graph No. 9:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/average%20age%20by%20year%20by%20gender.png)
## Bar graph No. 10:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/squat%20bench%20press%20deadlift%20by%20age%20group.png)
## Bar graph No. 11:
![alt_text](https://github.com/thatrandomobject/final_project_IPF/blob/main/charts/top%205%20strongest%20countries.png)

## Summary of Key Findings

  We found it interesting to group the powerlifters by gender and to see how their Relative Strength (RS) changes over chosen time (5 yrs.).  Where RS refers to the amount of force/ power a person can generate in relation to their body weight (Relative Strength Ratio=Total Strength/ Body Weight) and illustrates powerlifter’s efficiency and progress in a more objective manner. The first 2 linear graphs illustrate that in time the RS grows almost gradually in both groups, and the difference between male and female groups is not that big. We could state that the efficiency of the individuals in Weightlifting sport is increasing over time.

  The 3rd and 4th graphs support the outcome of the first 2 linear graphs. Total strength (combined amount of weight lifted by a powerlifter across three specific lifts: Squat, Bench, and Deadlift) seems to also grow gradually in male and female groups over chosen time period. Which results that efficiency of powerlifters in both gender groups grows due to growing total strength. The 12-month forecast (projection) based on the data collected during the project shows that these growth trends persist (graphs No. 5 and No. 6).

  Further we chose to count all the powerlifters who were active in competitions in the same chosen time frame of 5 years. It was interesting to observe a quite sharp drop down in 2020 and 2022. COVID pandemic obviously influenced the results of 2020. We decided to check our hypothesis for 2022 by looking into the count of the powerlifters across the countries (Map graph No. 8), and the results showed that number of active powerlifters dropped down in Ukraine and Russia, when normally the numbers of individuals in mentioned countries are high. Data confirmed that the results of 2022 were affected by the war in Ukraine. 

  The graphs No. 9, No. 10, and No. 11 are about interesting facts to know: 

  The average age is higher in females’ group then in men’s over the comparative time period of 5 sequent yrs (No. 9).
  
  The average of Total Strength among different age groups of the powerlifters across three specific lifts (Squat, Bench, and Deadlift). Data from 2023 suggests (No. 10). Are you up for Deadlift in your age group?
  
  Where the strongest powerlifters live? Bar graph No. 11 with TOP 5 Countries to look into based on data from 2023.




