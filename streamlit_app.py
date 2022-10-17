import streamlit # emoji's, etc. 
import pandas # read csv, etc. 
import requests # fruityvice api respnse
import snowflake.connector
from urllib.error import URLError # needed for control of flow
streamlit.title('Title Line A One')

streamlit.header('Header One 1')

streamlit.text('Text aaAAA')
streamlit.text('Text  bbBBBB')
streamlit.text('Text cc CCCC')

streamlit.header('\N{flexed biceps} Champion reference here \N{flexed biceps}')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# make picklist
fruits_selected = streamlit.multiselect("select item here:", list(my_fruit_list.index),['Kiwifruit','Avocado'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Filtered List: 
streamlit.dataframe(fruits_to_show) 
# full list:
# streamlit.header('Full List')
# streamlit.dataframe(my_fruit_list)
# fruit_choice = streamlit.text_input('enter a fruit?','Kiwi')  # make a default to avoid an error message
streamlit.header(' begin try / except with nested if-else ')
try: 
    fruit_choice = streamlit.text_input('enter a fruit?')  # make a default to avoid an error message
    streamlit.write('The user entered ', fruit_choice)
    if not fruit_choice: 
        streamlit.error(" Err msg 1- needed fruit entry. " )
    else: 
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        # streamlit.text(fruityvice_response) # response code 200
        # streamlit.text(fruityvice_response.json()) # writes raw json to screen
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized) # writes response as a table

except URLError as e: 
    streamlit.error()

streamlit.header(' begin snowflake connect ')
    
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("test data retrned from Snowflake:")
streamlit.dataframe(my_data_rows)

record_to_add = streamlit.text_input('enter a record to add','jackfruit')  # make a default to avoid an error message
streamlit.write('recrod to add here: ', record_to_add)
my_cur.execute("insert into fruit_load_list values ('from streamlit')") # need to fix this later


