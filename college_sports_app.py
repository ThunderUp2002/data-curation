import streamlit as st
import pandas as pd
# import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

file_path = "all_stats.csv"
all_stats_df = load_data(file_path)

st.title("[INSERT TITLE HERE]")

overall_tab, football_tab, volleyball_tab, soccer_tab = st.tabs(["Overall", "Football", "Volleyball", "Soccer"])

def filter_colleges_by_sport(df, cols):
    return df.dropna(subset=cols)

with overall_tab:
    st.header("Overall Stats")

    format_option = st.radio(
        "Format",
        ["All", "Conference", "College"],
        index=None,
        horizontal=True,
        label_visibility="collapsed"
    )

    if format_option == "All":
        with st.expander("See table"):
            all_stats_df.sort_values("Avg_Z_Score", ascending=False, inplace=True)
            all_stats_df.reset_index(drop=True, inplace=True)
            all_stats_df.index = all_stats_df.index + 1
            st.dataframe(all_stats_df)

    if format_option == "Conference":
        p4_conferences_dict = {
            "ACC": ["Boston College", "California", "Clemson", "Duke", "Florida St.", "Georgia Tech", "Louisville", "Miami (FL)", "North Carolina", "NC State", "Notre Dame", "Pittsburgh", "SMU", "Stanford", "Syracuse", "Virginia", "Virginia Tech", "Wake Forest"],
            "Big Ten": ["Illinois", "Indiana", "Iowa", "Maryland", "Michigan", "Michigan St.", "Minnesota", "Nebraska", "Northwestern", "Ohio St.", "Oregon", "Penn St.", "Purdue", "Rutgers", "Southern California", "UCLA", "Washington", "Wisconsin"],
            "Big 12": ["Arizona", "Arizona St.", "Baylor", "BYU", "Cincinnati", "Colorado", "Houston", "Iowa St.", "Kansas", "Kansas St.", "Oklahoma St.", "TCU", "Texas Tech", "UCF", "Utah", "West Virginia"],
            "SEC": ["Alabama", "Arkansas", "Auburn", "Florida", "Georgia", "Kentucky", "LSU", "Mississippi St.", "Missouri", "Oklahoma", "Ole Miss", "South Carolina", "Tennessee", "Texas", "Texas A&M", "Vanderbilt"]
            }
        p4_conferences_list = p4_conferences_dict.keys
        with st.popover("Select conference(s)"):
            acc = st.checkbox("ACC")
            big_ten = st.checkbox("Big Ten")
            big_12 = st.checkbox("Big 12")
            sec = st.checkbox("SEC")

    if format_option == "College":
        colleges = all_stats_df["Team"].sort_values()
        selected_college = st.selectbox(
        "Select a college",
        colleges,
        index=None,
        placeholder="Select a college",
        label_visibility="collapsed"
        )
        college_df = all_stats_df[all_stats_df["Team"] == selected_college]
        if selected_college is not None:
            st.dataframe(college_df)
    
    # If selected_college is None and selected conference is None, insert graph of average z-score distribution
    # Else display bar graph of college's z-score for each metric and average z-score

with football_tab:
    st.header("Football Stats")
    # Insert check box for conference
    # If selection is None, display graph of metric distribution for all teams
    # If selection is one or more conferences, display graph of that conference's metric distribution
    # Graph with checkbox for conferences and popover with checkbox for teams
    football_cols = ["+/- PPG", "+/- PPG Z-Score"]
    with st.expander("See table"):
        football_df = filter_colleges_by_sport(all_stats_df, football_cols)
        football_df.sort_values("+/- PPG", ascending=False, inplace=True)
        football_df.reset_index(inplace=True)
        football_df.index = football_df.index + 1
        st.dataframe(football_df[["Team"] + football_cols])

with volleyball_tab:
    st.header("Volleyball Stats")
    # Insert graph
    volleyball_cols = ["+/- Hitting %", "+/- Hitting % Z-Score"]
    with st.expander("See table"):
        volleyball_df = filter_colleges_by_sport(all_stats_df, volleyball_cols)
        volleyball_df.sort_values("+/- Hitting %", ascending=False, inplace=True)
        volleyball_df.reset_index(inplace=True)
        volleyball_df.index = volleyball_df.index + 1
        st.dataframe(volleyball_df[["Team"] + volleyball_cols])

with soccer_tab:
    st.header("Soccer Stats")
    # Insert graph
    soccer_cols = ["+/- GPG", "+/- GPG Z-Score"]
    with st.expander("See table"):
        soccer_df = filter_colleges_by_sport(all_stats_df, soccer_cols)
        soccer_df.sort_values("+/- GPG", ascending=False, inplace=True)
        soccer_df.reset_index(inplace=True)
        soccer_df.index = soccer_df.index + 1
        st.dataframe(soccer_df[["Team"] + soccer_cols])