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

streamlit.header(' begin function code here ')
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # streamlit.text(fruityvice_response) # response code 200
    # streamlit.text(fruityvice_response.json()) # writes raw json to screen
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # streamlit.dataframe(fruityvice_normalized) # writes response as a table       
    return fruityvice_normalized

streamlit.header(' begin try / except with nested if-else ')
try: 
    fruit_choice = streamlit.text_input('enter a fruit?')  # make a default to avoid an error message
    streamlit.write('The user entered ', fruit_choice)
    if not fruit_choice: 
        streamlit.error(" Err msg 1- needed fruit entry. " )
    else: 
        back_from_function = get_fruityvice_data(fruit_choice)

except URLError as e: 
    streamlit.error()

streamlit.header(' begin snowflake connect ')
# snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

# add a button to load the data
if streamlit.button('Get f Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    # my_data_rows = my_cur.fetchall()
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.header("test data retrned from Snowflake:")
    streamlit.dataframe(my_data_rows)    
    # my_cur = my_cnx.cursor()

# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

streamlit.header(" begin data to add section ")
def insert_row_snowflake(new_fruit): 
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')") # now takes variable
        return "added new data " + new_fruit
    
add_my_fruit = streamlit.text_input('enter a record to add')  # make a default to avoid an error message
if streamlit.button('Add frt to table '):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
    
# streamlit.write('recrod to add here: ', record_to_add)
