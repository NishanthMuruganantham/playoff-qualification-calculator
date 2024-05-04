import streamlit as st
from src.views.custom_schedule.custom_schedule import simulate_the_qualification_for_custom_schedule
from src.views.homepage import homepage
from src.views.tournament import simulate_for_ipl

st.set_page_config(
    # initial_sidebar_state="expanded",
    layout="wide",
    page_title="Playoff Qualification Scenario Generator",
    page_icon=":soccer:",
)


page_names_to_funcs = {
    "Home": homepage,
    "Indian Premier League (IPL)": simulate_for_ipl,
    "Custom Schedule": simulate_the_qualification_for_custom_schedule
}

demo_name = st.sidebar.selectbox("Pages", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
