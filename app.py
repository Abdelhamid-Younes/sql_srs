# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "sql_tables_exercise.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/sql_tables_exercise.duckdb", read_only=False)

with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review ?",
        available_themes_df["theme"],
        index=None,
        placeholder="Select a theme ...",
    )
    if theme:
        st.write("You selected:", theme)
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = f"SELECT * FROM memory_state"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_review")
        .reset_index(drop=True)
    )
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
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table : {table}")
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)

with tab3:
    st.text(answer)
