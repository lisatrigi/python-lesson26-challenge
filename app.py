import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

st.title("Fitness Tracker")
def get_data():
    conn = sqlite3.connect("workouts.db")
    df = pd.read_sql_query("SELECT * FROM workouts ORDER BY date DESC", conn)
    conn.close()
    return df

def add_data(exercise, weight, reps, date):
    conn = sqlite3.connect("workouts.db")
    conn.execute(
        "INSERT INTO workouts (exercise, weight, reps, date) VALUES (?, ?, ?, ?)",
        (exercise, weight, reps, date),
    )
    conn.commit()
    conn.close()

st.header("add workout")
exercise = st.text_input("exercise name")
weight = st.number_input("weight (kg)", min_value=0.0)
reps = st.number_input("reps", min_value=0)
date = st.date_input("date", datetime.now())

if st.button("add workout"):
    if exercise:
        add_data(exercise, weight, reps, str(date))
        st.success("workout added")
    else:
        st.warning("enter an exercise name")

st.header("workout history")
data = get_data()

if len(data) > 0:
    st.dataframe(data)

    st.header("Progress chart")
    exercises = data["exercise"].unique()
    chosen_exercise = st.selectbox("select exercise", exercises)
    ex_data = data[data["exercise"] == chosen_exercise]

    ex_data = ex_data.sort_values("date")

    plt.figure(figsize=(6, 3))
    plt.plot(ex_data["date"], ex_data["weight"], marker="o", label="Weight (kg)")
    plt.title(chosen_exercise + " Progress")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)
else:
    st.info("no workouts yet, add one above")
