import pandas as pd
import streamlit as st


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
