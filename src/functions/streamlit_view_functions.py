import pandas as pd
import streamlit as st
from typing import Dict
from points_table_simulator import PointsTableSimulator


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
        points_table_df_column.dataframe(current_points_table, hide_index=True)

def _get_inputs_to_generate_qualification_scenarios(points_table_simulator: PointsTableSimulator) -> Dict[str, int]:
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
        st.form_submit_button("Submit")
    return {
        "selected_team_to_generate_qualification_scenarios": selected_team,
        "expected_position_in_the_points_table": expected_position_in_the_points_table,
        "number_of_qualification_scenarios": number_of_qualification_scenarios,
        "generate_qualification_scenarios_inputs_submitted": True
    }
