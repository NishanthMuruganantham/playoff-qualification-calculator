import time
from typing import Dict, List, Optional
import pandas as pd
import streamlit as st
from points_table_simulator import PointsTableSimulator
from points_table_simulator.exceptions import (
    NoQualifyingScenariosError,
    TournamentCompletionBelowCutoffError
)


def _display_given_fixture_and_current_points_table(
    current_points_table: pd.DataFrame, remaining_fixture: pd.DataFrame, expanded: bool = False
):
    action = "expand" if not expanded else "collapse"
    """Display the given fixture and current points table."""
    with st.expander(f"**Click here to {action} given fixture and current points table**", expanded=expanded):
        st.write("")
        schedule_df_column, points_table_df_column = st.columns(2, gap="small")
        schedule_df_column.markdown("<h5 style='color: #1e90ff; text-align: center'>Remaining Fixture</h5>", unsafe_allow_html=True)
        st.write("")
        schedule_df_column.dataframe(remaining_fixture, hide_index=True)
        points_table_df_column.markdown("<h5 style='color: #1e90ff; text-align: center'>Current Points Table</h5>", unsafe_allow_html=True)
        st.write("")
        rename_dict = {column: column.replace("matches_", "") for column in current_points_table.columns if column != "team"}
        current_points_table = current_points_table.rename(rename_dict, axis=1)
        points_table_df_column.dataframe(current_points_table, hide_index=True)


def _display_qualification_scenarios(
    list_of_points_tables: List[pd.DataFrame],
    list_of_qualification_scenarios: List[pd.DataFrame],
    selected_team: str,
    away_team_column_name: Optional[str] = "team_2",
    home_team_column_name: Optional[str] = "team_1"
):
    """Display the qualification scenarios."""
    for scenario_no, (points_table, schedule) in enumerate(zip(list_of_points_tables, list_of_qualification_scenarios)):
        with st.expander(f"**Click here to expand qualification scenario {scenario_no + 1}**"):
            st.write("")
            st.markdown(f"<h3 style='color: #1e90ff;'>Qualification Scenario {scenario_no + 1}:</h3>", unsafe_allow_html=True)
            st.write("")
            qualification_fixture_column, qualification_points_table_column = st.columns(2, gap="small")
            qualification_fixture_column.markdown("<p style='font-weight: bold; color: #4CAF50;'>Remaining Fixture Favourable Outcome</p>", unsafe_allow_html=True)
            qualification_fixture_column.dataframe(
                schedule.style.apply(
                    lambda row: [
                        'background-color: CornflowerBlue;' if row[
                            away_team_column_name
                        ] == selected_team or row[
                            home_team_column_name
                        ] == selected_team else '' for _ in row
                    ],
                    axis=1
                ),
                hide_index=True
            )
            qualification_points_table_column.markdown("<p style='font-weight: bold; color: #4CAF50;'>Points Table</p>", unsafe_allow_html=True)
            rename_dict = {column: column.replace("matches_", "") for column in points_table.columns if column != "team"}
            points_table = points_table.rename(rename_dict, axis=1)
            points_table = points_table[["team", "played", "won", "lost", "points"]]
            qualification_points_table_column.dataframe(
                points_table.style.apply(
                    lambda row: ['background-color: CornflowerBlue;' if row["team"] == selected_team else '' for _ in row],
                    axis=1
                ),
                hide_index=True
            )
            time.sleep(1)
            st.write("")


def _generate_qualification_scenarios(points_table_simulator: PointsTableSimulator):
    _session_state = {
        "generate_qualification_scenarios_inputs_submitted" : False
    }
    try:
        inputs_for_generating_qualification_scenarios = _get_inputs_to_generate_qualification_scenarios(points_table_simulator)
        if inputs_for_generating_qualification_scenarios["generate_qualification_scenarios_inputs_submitted"]:
            _session_state["generate_qualification_scenarios_inputs_submitted"] = True

        if _session_state["generate_qualification_scenarios_inputs_submitted"]:
            list_of_points_tables = []
            list_of_qualification_scenarios = []
            start_time = time.time()
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
                    {inputs_for_generating_qualification_scenarios['selected_team_to_generate_qualification_scenarios']}</b>\
                        to be placed within <b>top {inputs_for_generating_qualification_scenarios['expected_position_in_the_points_table']}\
                            position</b> in the points table </p><hr>",
                unsafe_allow_html=True
            )
            if list_of_points_tables:
                end_time = time.time()
                _display_qualification_scenarios(
                    list_of_points_tables,
                    list_of_qualification_scenarios,
                    inputs_for_generating_qualification_scenarios["selected_team_to_generate_qualification_scenarios"],
                )
                st.write(f"Time taken to generate the qualification scenarios: {round(end_time - start_time, 2)} seconds")
                list_of_points_tables = []

    except NoQualifyingScenariosError as no_qualifying_scenarios_error:
        st.error(
            f"Error: No qualifying scenarios found for the given team '{no_qualifying_scenarios_error.team_name}' at \
                position '{no_qualifying_scenarios_error.points_table_position}' in the points table",
            icon="⚠️"
        )
    except TournamentCompletionBelowCutoffError as exception:
        st.error(
            f"Only {exception.tournament_completion_percentage}% of the tournament has completed. The tournament \
                should atleast be {exception.cutoff_percentage}% completed to check for the qualification scenarios",
                icon="⚠️"
        )


def _get_inputs_to_generate_qualification_scenarios(points_table_simulator: PointsTableSimulator) -> Dict:
    """Get inputs to generate qualification scenarios."""
    with st.form(key="select_team_to_generate_qualification_scenarios"):
        selected_team = st.selectbox(
            label="Select Team to generate qualification scenarios",
            options=points_table_simulator.available_teams_in_fixture,
            help="Select the team you want to generate the qualification scenarios",
        )
        input_column_1, input_column_2 = st.columns(2, gap="small")
        expected_position_in_the_points_table = input_column_1.number_input(
            "Your expected position in the points table",
            max_value=len(points_table_simulator.current_points_table) + 1,
            min_value=1,
            value=4,
        )
        number_of_qualification_scenarios = input_column_2.number_input(
            "Number of qualification scenarios to generate",
            max_value=10,
            min_value=1,
            value=4,
            help="Select the number of qualification scenarios you want to generate",
            key="number_of_qualification_scenarios"
        )
        is_form_submitted = st.form_submit_button("Submit")
    return {
        "selected_team_to_generate_qualification_scenarios": selected_team,
        "expected_position_in_the_points_table": expected_position_in_the_points_table,
        "number_of_qualification_scenarios": number_of_qualification_scenarios,
        "generate_qualification_scenarios_inputs_submitted": True if is_form_submitted else False
    }
