import streamlit as st
import pandas as pd
import duckdb
import io

csv='''
beverage, price
orange juice, 2.5
Expresso, 2
Tea, 3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
foodt_item, food_price
cookie juice, 2.5
chocolatine, 2
muffin, 3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

with st.sidebar:
    option = st.selectbox(
        'What would you like to review ?',
        ['Joins', 'Group By', 'Windows Functions'],
        index=None,
        placeholder="Select a theme ...",
    )
    st.write('You selected:', option)

solution = duckdb.sql(answer).df()

st.header("Enter you code:")
query = st.text_area(label="Your SQL code here", key="user_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("Table : beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution)

with tab3:
    st.write(answer)