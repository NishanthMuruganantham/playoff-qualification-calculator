from src.functions.fixture_collector import get_fixture_for_given_tournament
from src.views.custom_schedule.custom_schedule import _apply_banner_styles, _create_banner
import streamlit as st
from points_table_simulator import PointsTableSimulator
from src.functions.streamlit_view_functions import (
    _display_given_fixture_and_current_points_table,
    _get_inputs_to_generate_qualification_scenarios
)


def simulate_for_ipl():
    session_state = {
        "generate_qualification_scenarios_inputs_submitted": False
    }
    tournament_df = None
    _apply_banner_styles()
    _create_banner(subtitle="For Indian Premier League")
    st.write("")
    with st.balloons():
        tournament_df = get_fixture_for_given_tournament(1410320)
        points_table_simulator = PointsTableSimulator(
            tournament_schedule=tournament_df,
            points_for_a_win=2,
            tournament_schedule_away_team_column_name="team_2",
            tournament_schedule_home_team_column_name="team_1",
        )
        _display_given_fixture_and_current_points_table(
            current_points_table=points_table_simulator.current_points_table,
            expanded=True,
            remaining_fixture=tournament_df,
        )

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
