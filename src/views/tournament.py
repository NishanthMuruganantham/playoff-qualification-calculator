import streamlit as st
from points_table_simulator import PointsTableSimulator
from src.functions.fixture_collector import get_fixture_for_given_tournament
from src.functions.streamlit_view_functions import (
    _display_given_fixture_and_current_points_table,
    _generate_qualification_scenarios
)
from src.views.custom_schedule.custom_schedule import (
    _apply_banner_styles,
    _create_banner
)


def simulate_for_ipl():
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

    _generate_qualification_scenarios(points_table_simulator)
