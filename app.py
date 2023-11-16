# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st
import ast


con = duckdb.connect(database="data/sql_tables_exercice", read_only=False)

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ["Cross_joins", "Group By", "window_functions"],
        index=None,
        placeholder="Select a theme ...",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter you code:")
query = st.text_area(label="Your SQL code here", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))

    except KeyError as error:
        st.write("There arte some missing columns !")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(f"result has a {n_lines_difference} lines difference with solution_df")

tab2, tab3 = st.tabs(["Tables", "Solution"])
#
with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"Table : {table}")
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)

with tab3:
    st.write(answer)
