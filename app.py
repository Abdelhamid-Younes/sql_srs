# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st


con = duckdb.connect(database="data/sql_tables_exercice", read_only=False)

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ["Cross_joins", "Group By", "Windows Functions"],
        index=None,
        placeholder="Select a theme ...",
    )
    st.write("You selected:", theme)

    exercice = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercice)

#solution_df = duckdb.sql(ANSWER_STR).df()

st.header("Enter you code:")
query = st.text_area(label="Your SQL code here", key="user_input")
# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)
#
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#
#     except KeyError as error:
#         st.write("There arte some missing columns !")
#
#     n_lines_difference = result.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(f"result has a {n_lines_difference} lines difference with solution_df")
#
# tab2, tab3 = st.tabs(["Tables", "Solution"])
#
# with tab2:
#     st.write("Table : beverages")
#     st.dataframe(beverages)
#     st.write("Table: food_items")
#     st.dataframe(food_items)
#     st.write("Expected:")
#     st.dataframe(solution_df)
#
# with tab3:
#     st.write(ANSWER_STR)
