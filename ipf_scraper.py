import configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import psycopg2

# setting up parameters to be taken from a local file, so that password and other connection details are not public
config = configparser.ConfigParser()
config.read('config.ini')
host = config['database']['host']
database = config['database']['database']
user = config['database']['user']
password = config['database']['password']

# creating a connection and table creation query
connection = psycopg2.connect(database=database, host=host, user=user, password=password)
cursor = connection.cursor()
create_table_query = """
    CREATE TABLE IF NOT EXISTS open_ipf_test(
    rank INT,
    athlete_name VARCHAR,
    federation VARCHAR,
    event_date DATE,
    home VARCHAR,
    sex VARCHAR,
    age VARCHAR,
    equip VARCHAR,
    weight_class VARCHAR,
    weight VARCHAR,
    squat VARCHAR,
    bench_press VARCHAR,
    deadlift VARCHAR,
    total VARCHAR,
    glp_score VARCHAR)    
    """
cursor.execute(create_table_query)

start = time.time()
url = 'https://www.openipf.org/'
scraped_data = []
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

service.start()
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((
    By.CLASS_NAME, 'ui-widget-content '
)))
# find maximum height of scroll
max_height = driver.execute_script('return document.querySelector("div.slick-viewport-left:nth-child(3)").scrollHeight')
# start of data heights
height_of_data = 0
# a list to save ranks which have already been read in
rank_list = []
while height_of_data < max_height - 25:
    # wait for all the data elements to be loaded in
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
        By.CLASS_NAME, 'slick-cell')))
    # selecting the element which needs to be scrolled
    table_element = driver.find_element(By.XPATH, '//*[@id="theGrid"]/div[4]/div[3]')
    # waiting some time after scrolling; was not working without it
    time.sleep(3)
    # selecting all the rows that contain data
    data = driver.find_elements(By.CLASS_NAME, 'ui-widget-content ')
    for stats in data:
        # find the height of each row of data, convert it to float for comparison to maximum height
        height_of_data = float(stats.get_attribute('style').split(' ')[1].replace('px', '')
                               .replace(';', ''))
        # define in which class the rank data is stored
        rank = stats.find_element(By.CLASS_NAME, 'slick-cell.l1.r1').text
        # if statement is used to check if the data had already been scraped for this rank (so no duplicates are added)
        if rank not in rank_list:
            # if a rank has not been in the list before - append it to the rank_list
            rank_list.append(rank)
            # define all the different classes of data and what to do if they are empty strings
            if rank == '':
                rank = None
            name = stats.find_element(By.CLASS_NAME, 'slick-cell.l2.r2').text
            if name == '':
                name = None
            federation = stats.find_element(By.CLASS_NAME, 'slick-cell.l3.r3').text
            if federation == '':
                federation = None
            date = stats.find_element(By.CLASS_NAME, 'slick-cell.l4.r4').text
            if date == '':
                date = None
            home = stats.find_element(By.CLASS_NAME, 'slick-cell.l5.r5').text
            if home == '':
                home = None
            sex = stats.find_element(By.CLASS_NAME, 'slick-cell.l6.r6').text
            if sex == '':
                sex = None
            age = stats.find_element(By.CLASS_NAME, 'slick-cell.l7.r7').text
            if age == '':
                age = None
            equip = stats.find_element(By.CLASS_NAME, 'slick-cell.l8.r8').text
            if equip == '':
                equip = None
            weight_class = stats.find_element(By.CLASS_NAME, 'slick-cell.l9.r9').text
            if weight_class == '':
                weight_class = None
            weight = stats.find_element(By.CLASS_NAME, 'slick-cell.l10.r10').text
            if weight == '':
                weight = None
            squat = stats.find_element(By.CLASS_NAME, 'slick-cell.l11.r11').text
            if squat == '':
                squat = None
            bench = stats.find_element(By.CLASS_NAME, 'slick-cell.l12.r12').text
            if bench == '':
                bench = None
            deadlift = stats.find_element(By.CLASS_NAME, 'slick-cell.l13.r13').text
            if deadlift == '':
                bench = None
            total = stats.find_element(By.CLASS_NAME, 'slick-cell.l14.r14').text
            if total == '':
                total = None
            glp_score = stats.find_element(By.CLASS_NAME, 'slick-cell.l15.r15').text
            if glp_score == '':
                glp_score = None
            # create a dictionary for each row of data, to be further added to list scraped_data
            scraped_data.append({
                'Rank': rank,
                'Name': name,
                'Federation': federation,
                'Date': date,
                'Home': home,
                'Sex': sex,
                'Age': age,
                'Equip': equip,
                'Weight class': weight_class,
                'Weight': weight,
                'Squat': squat,
                'Bench press': bench,
                'Deadlift': deadlift,
                'Total': total,
                'GLP': glp_score
            })
            # definition of insert to SQL table
            insert_query = ('INSERT INTO open_ipf_test('
                            'rank, athlete_name, federation, event_date, home, sex, age, equip, weight_class,'
                            'weight, squat, bench_press, deadlift, total, glp_score) VALUES('
                            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
            # executing the insert_query
            cursor.execute(insert_query, (rank, name, federation, date, home, sex, age, equip, weight_class, weight,
                                          squat, bench, deadlift, total, glp_score))
        else:
            # text that is printed if rank had already been in the rank_list
            print(f'Data already scraped for: {rank}')
    # commiting the data from the insert query
    connection.commit()
    # scrolling the element
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                          table_element)
# closes browser once finished
driver.quit()

# creates a dataframe of scraped_data
df = pd.DataFrame(scraped_data)
# creates a csv file of scraped_data with no additional index column
df.to_csv('IPF_data.csv', index=False)  # done to create a csv file to have alongside SQL query
# gives variable end a value of time once the process is finished
end = time.time()
# calculates the duration it took to scrape the data
duration = end-start
# prints additional text about start tame and end time as well as duration in minutes
print(f'Whole website was scraped.\nTime of start {start}.\nTime of end {end}.\nIt took {duration/3600} minutes.')
