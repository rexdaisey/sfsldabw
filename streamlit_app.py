import streamlit # emoji's, etc. 
import pandas # read csv, etc. 

streamlit.title('Title Line A One')

streamlit.header('Header One 1')

streamlit.text('Text aaAAA')
streamlit.text('Text  bbBBBB')
streamlit.text('Text cc CCCC')

streamlit.header('\N{flexed biceps} Champion reference here \N{flexed biceps}')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# make picklist
streamlit.multiselect("select item here:", list(my_fruit_list.index),['Kiwifruit','Avocado'])

streamlit.dataframe(my_fruit_list)



