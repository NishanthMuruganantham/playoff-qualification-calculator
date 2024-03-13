import streamlit as st
from points_table_simulator.points_table_simulator import PointsTableSimulator
from points_table_simulator.exceptions import InvalidColumnNamesError
import pandas as pd


session_state = {
    "column_name_input_form_submitted": False,
}

def _apply_banner_styles():
    st.markdown(
        """
        <style>
            .banner {
                background-color: #4CAF50;
                padding: 40px 20px;
                text-align: center;
                margin-bottom: 30px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .title {
                color: white;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .subtitle {
                color: white;
                font-size: 28px;
                margin-bottom: 20px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }
            .description {
                color: white;
                font-size: 20px;
                line-height: 1.5;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _create_banner():
    st.markdown(
        """
        <div class="banner">
            <div class="title">🏆⚽ Qualification Scenario Generator ⚽🏆</div>
            <div class="subtitle">📊 Calculate qualification scenarios for your own tournament fixture 📊</div>
            <p class="description">📂 Upload your tournament fixture and calculate the various possible qualification scenarios for your favourite team 📈</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _create_column_name_inputs_form():
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <p style="font-size: 18px; font-style: italic; color: #4CAF50;">Please enter the names for the respective columns in your fixture if they are different from the below defaults</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    input_column_1, input_column_2, input_column_3, input_column_4 = st.columns(4, gap="small")
    home_team_column_name = input_column_1.text_input("Home team column name", value="Home")
    away_team_column_name = input_column_2.text_input("Away team column name", value="Away")
    winner_team_column_name = input_column_3.text_input("Winner team column name", value="Winner")
    match_number_column_name = input_column_4.text_input("Match number column name", value="Match No")

    input_column_5, input_column_6, input_column_7 = st.columns(3, gap="small")
    points_for_a_win = input_column_5.number_input("Points for a win", min_value=1, value=2)
    points_for_a_draw = input_column_6.number_input("Points for a draw", min_value=0, value=1)
    points_for_a_no_result = input_column_7.number_input("Points for a no result", min_value=0, value=1)

    st.write("")

    return {
        "home_team_column_name": home_team_column_name,
        "away_team_column_name": away_team_column_name,
        "winner_team_column_name": winner_team_column_name,
        "match_number_column_name": match_number_column_name,
        "points_for_a_win": points_for_a_win,
        "points_for_a_draw": points_for_a_draw,
        "points_for_a_no_result": points_for_a_no_result,
    }

def simulate_the_qualification_for_custom_schedule():
    _apply_banner_styles()
    _create_banner()
    fixture = st.file_uploader("Upload the CSV file", type="csv", key="file_uploader", accept_multiple_files=False, help="Please upload your tournament fixture file in CSV format.")

    if fixture:
        with st.form(key="column_name_inputs_form", clear_on_submit=True):
            column_name_inputs = _create_column_name_inputs_form()
            column_name_inputs_form_submit_button_clicked = st.form_submit_button("Submit")

        if column_name_inputs_form_submit_button_clicked:
            session_state["column_name_input_form_submitted"] = True
            session_state.update(
                column_name_inputs
            )

        if session_state["column_name_input_form_submitted"]:
            st.write("")
            uploaded_fixture_df = pd.read_csv(fixture)
            try:
                points_table_simulator = PointsTableSimulator(
                    tournament_schedule=uploaded_fixture_df,
                    points_for_a_win=session_state["points_for_a_win"],
                    tournament_schedule_away_team_column_name=session_state["away_team_column_name"],
                    tournament_schedule_home_team_column_name=session_state["home_team_column_name"],
                    tournament_schedule_winning_team_column_name=session_state["winner_team_column_name"],
                    tournament_schedule_match_number_column_name=session_state["match_number_column_name"],
                )

            except InvalidColumnNamesError as column_name_error:
                st.error(f"Error: Given column '{column_name_error.column_value}' is not found in the given CSV", icon="⚠️")
