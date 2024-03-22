import streamlit as st
from src.views.custom_schedule.custom_schedule import simulate_the_qualification_for_custom_schedule
from src.views.homepage import homepage

st.set_page_config(layout="wide")


page_names_to_funcs = {
    "Home": homepage,
    "custom": simulate_the_qualification_for_custom_schedule
}

demo_name = st.sidebar.selectbox("Pages", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
