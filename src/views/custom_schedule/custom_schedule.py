from typing import Dict
import streamlit as st
import pandas as pd
from points_table_simulator.points_table_simulator import PointsTableSimulator
from points_table_simulator.exceptions import InvalidColumnNamesError, InvalidScheduleDataError, NoQualifyingScenariosError
from src.functions.streamlit_view_functions import (
    _display_given_fixture_and_current_points_table,
    _display_qualification_scenarios,
    _get_inputs_to_generate_qualification_scenarios
)
from src.static._styles import _apply_banner_styles, _create_banner


session_state = {
    "column_name_input_form_submitted": False,
    "generate_qualification_scenarios_inputs_submitted": False,
}

def _create_column_name_inputs_form() -> Dict[str, str]:
    """Create form inputs for custom column names."""
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
    """Main function to simulate qualification scenarios for a custom schedule."""
    _apply_banner_styles()
    _create_banner()
    fixture = st.file_uploader("Upload the CSV file", type="csv", key="file_uploader", accept_multiple_files=False, help="Please upload your tournament fixture file in CSV format.")

    if fixture:
        with st.form(key="column_name_inputs_form", clear_on_submit=True):
            column_name_inputs = _create_column_name_inputs_form()
            column_name_inputs_form_submit_button_clicked = st.form_submit_button("Submit")

        if column_name_inputs_form_submit_button_clicked:
            session_state["column_name_input_form_submitted"] = True
            session_state.update(column_name_inputs)

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

                _display_given_fixture_and_current_points_table(points_table_simulator.current_points_table, uploaded_fixture_df)

                inputs_for_generating_qualification_scenarios = _get_inputs_to_generate_qualification_scenarios(points_table_simulator)

                if inputs_for_generating_qualification_scenarios["generate_qualification_scenarios_inputs_submitted"]:
                    session_state["generate_qualification_scenarios_inputs_submitted"] = True

                if session_state["generate_qualification_scenarios_inputs_submitted"]:
                    with st.snow():
                        (
                            list_of_points_tables,
                            list_of_qualification_scenarios
                        ) = points_table_simulator.simulate_the_qualification_scenarios(
                            inputs_for_generating_qualification_scenarios["selected_team_to_generate_qualification_scenarios"],
                            inputs_for_generating_qualification_scenarios["expected_position_in_the_points_table"],
                            inputs_for_generating_qualification_scenarios["number_of_qualification_scenarios"]
                        )
                        st.markdown(
                            f"<p>Please find below the various qualification scenarios for <b>\
                                {inputs_for_generating_qualification_scenarios['selected_team_to_generate_qualification_scenarios']}</b></p><hr>",
                            unsafe_allow_html=True
                        )
                    _display_qualification_scenarios(
                        list_of_points_tables,
                        list_of_qualification_scenarios,
                        inputs_for_generating_qualification_scenarios["selected_team_to_generate_qualification_scenarios"],
                        session_state["away_team_column_name"],
                        session_state["home_team_column_name"]
                    )

            except InvalidColumnNamesError as column_name_error:
                st.error(f"Error: Given column '{column_name_error.column_value}' is not found in the given CSV", icon="⚠️")

            except InvalidScheduleDataError as schedule_data_error:
                st.error(f"Error: Given fixture has empty or Nan values in the '{schedule_data_error.column_name}' column", icon="⚠️")

            except NoQualifyingScenariosError as no_qualifying_scenarios_error:
                st.error(
                    f"Error: No qualifying scenarios found for the given team '{no_qualifying_scenarios_error.team_name}' at \
                        position '{no_qualifying_scenarios_error.points_table_position}' in the points table",
                    icon="⚠️"
                )
