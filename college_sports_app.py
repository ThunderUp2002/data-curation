import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

file_path = "all_stats.csv"
all_stats_df = load_data(file_path)

p4_conferences = {
            "ACC": ["Boston College", "California", "Clemson", "Duke", "Florida St.", "Georgia Tech", "Louisville", "Miami (FL)", "North Carolina", "NC State", "Notre Dame", "Pittsburgh", "SMU", "Stanford", "Syracuse", "Virginia", "Virginia Tech", "Wake Forest"],
            "Big Ten": ["Illinois", "Indiana", "Iowa", "Maryland", "Michigan", "Michigan St.", "Minnesota", "Nebraska", "Northwestern", "Ohio St.", "Oregon", "Penn St.", "Purdue", "Rutgers", "Southern California", "UCLA", "Washington", "Wisconsin"],
            "Big 12": ["Arizona", "Arizona St.", "Baylor", "BYU", "Cincinnati", "Colorado", "Houston", "Iowa St.", "Kansas", "Kansas St.", "Oklahoma St.", "TCU", "Texas Tech", "UCF", "Utah", "West Virginia"],
            "SEC": ["Alabama", "Arkansas", "Auburn", "Florida", "Georgia", "Kentucky", "LSU", "Mississippi St.", "Missouri", "Oklahoma", "Ole Miss", "South Carolina", "Tennessee", "Texas", "Texas A&M", "Vanderbilt"]
            }

acc_teams = all_stats_df[all_stats_df["Team"].isin(p4_conferences["ACC"])]
big_ten_teams = all_stats_df[all_stats_df["Team"].isin(p4_conferences["Big Ten"])]
big_12_teams = all_stats_df[all_stats_df["Team"].isin(p4_conferences["Big 12"])]
sec_teams = all_stats_df[all_stats_df["Team"].isin(p4_conferences["SEC"])]

st.title("College Sports Stats")

overall_tab, football_tab, volleyball_tab, soccer_tab = st.tabs(["Overall", "Football", "W Volleyball", "W Soccer"])

def filter_colleges_by_conferences(df, selected_conferences):
    if not selected_conferences:
        return df
    
    selected_colleges = []
    for conf in selected_conferences:
        selected_colleges.extend(p4_conferences[conf])

    return df[df["Team"].isin(selected_colleges)]

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
        ave_z_score_plot = px.histogram(all_stats_df, x="Avg_Z_Score", title="Distribution of Average z-Score")
        st.plotly_chart(ave_z_score_plot)
        with st.expander("See table"):
            all_stats_df.sort_values("Avg_Z_Score", ascending=False, inplace=True)
            all_stats_df.reset_index(drop=True, inplace=True)
            all_stats_df.index = all_stats_df.index + 1
            st.dataframe(all_stats_df)

    if format_option == "Conference":
               
        with st.popover("Select conference(s)"):
            acc = st.checkbox("ACC", key="acc_overall_checkbox")
            big_ten = st.checkbox("Big Ten", key="big_ten_overall_checkbox")
            big_12 = st.checkbox("Big 12", key="big_12_overall_checkbox")
            sec = st.checkbox("SEC", key="sec_overall_checkbox")
        
        selected_conferences = []
        selected_conference_teams = []

        if acc:
            selected_conferences.append("ACC")
            selected_conference_teams.append(acc_teams)
        if big_ten:
            selected_conferences.append("Big Ten")
            selected_conference_teams.append(big_ten_teams)
        if big_12:
            selected_conferences.append("Big 12")
            selected_conference_teams.append(big_12_teams)
        if sec:
            selected_conferences.append("SEC")
            selected_conference_teams.append(sec_teams)

        if len(selected_conferences) != 0:
            conference_df = filter_colleges_by_conferences(all_stats_df, selected_conferences)

            plt.figure(figsize=(10, 6))
            for conf_teams, conf_name in zip(selected_conference_teams, selected_conferences):
                sns.kdeplot(data=conf_teams, x="Avg_Z_Score", label=conf_name)
            plt.title("Average z-Score Distribution(s) for Selected Conference(s)")
            plt.xlabel("Average z-Score")
            plt.legend()
            st.pyplot(plt)

            with st.expander("See table"):
                st.dataframe(conference_df)

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
            # Display bar graph of each metric's z-score and average z-score for selected college
            # college_metrics_df = college_df[["Team", ""]]
            # overall_college_plot = px.bar(college_df, x=[""])
            st.dataframe(college_df)

with football_tab:
    st.header("Football Stats")

    with st.popover("Select conference(s)"):
        acc = st.checkbox("ACC", key="acc_football_checkbox")
        big_ten = st.checkbox("Big Ten", key="big_ten_football_checkbox")
        big_12 = st.checkbox("Big 12", key="big_12_football_checkbox")
        sec = st.checkbox("SEC", key="sec_football_checkbox")

    selected_conferences = []
    selected_conference_teams = []

    if acc:
        selected_conferences.append("ACC")
        selected_conference_teams.append(acc_teams)
    if big_ten:
        selected_conferences.append("Big Ten")
        selected_conference_teams.append(big_ten_teams)
    if big_12:
        selected_conferences.append("Big 12")
        selected_conference_teams.append(big_12_teams)
    if sec:
        selected_conferences.append("SEC")
        selected_conference_teams.append(sec_teams)

    football_cols = ["+/- PPG", "+/- PPG Z-Score"]
    football_df = filter_colleges_by_sport(all_stats_df, football_cols)
    football_df = filter_colleges_by_conferences(football_df, selected_conferences)
    football_df.sort_values("+/- PPG", ascending=False, inplace=True)
    football_df.reset_index(inplace=True)
    football_df.index = football_df.index + 1

    if len(selected_conferences) == 0:
        football_metric_plot = px.histogram(football_df, x="+/- PPG", title="Distribution of +/- PPG for All Teams")
        st.plotly_chart(football_metric_plot)

    else:
        plt.figure(figsize=(10, 6))
        for conf_teams, conf_name in zip(selected_conference_teams, selected_conferences):
            sns.kdeplot(data=conf_teams, x="+/- PPG", label=conf_name)
        plt.title("Average +/- PPG Distribution(s) for Selected Conference(s)")
        plt.xlabel("Average +/- PPG")
        plt.legend()
        st.pyplot(plt)
    
    with st.expander("See table"):
        st.dataframe(football_df[["Team"] + football_cols])

with volleyball_tab:
    st.header("W Volleyball Stats")

    with st.popover("Select conference(s)"):
        acc = st.checkbox("ACC", key="acc_volleyball_checkbox")
        big_ten = st.checkbox("Big Ten", key="big_ten_volleyball_checkbox")
        big_12 = st.checkbox("Big 12", key="big_12_volleyball_checkbox")
        sec = st.checkbox("SEC", key="sec_volleyball_checkbox")

    selected_conferences = []
    selected_conference_teams = []

    if acc:
        selected_conferences.append("ACC")
        selected_conference_teams.append(acc_teams)
    if big_ten:
        selected_conferences.append("Big Ten")
        selected_conference_teams.append(big_ten_teams)
    if big_12:
        selected_conferences.append("Big 12")
        selected_conference_teams.append(big_12_teams)
    if sec:
        selected_conferences.append("SEC")
        selected_conference_teams.append(sec_teams)

    volleyball_cols = ["+/- Hitting %", "+/- Hitting % Z-Score"]
    volleyball_df = filter_colleges_by_sport(all_stats_df, volleyball_cols)
    volleyball_df = filter_colleges_by_conferences(volleyball_df, selected_conferences)
    volleyball_df.sort_values("+/- Hitting %", ascending=False, inplace=True)
    volleyball_df.reset_index(inplace=True)
    volleyball_df.index = volleyball_df.index + 1

    if len(selected_conferences) == 0:
        volleyball_metric_plot = px.histogram(volleyball_df, x="+/- Hitting %", title="Distribution of +/- Hitting Pct. for All Teams")
        st.plotly_chart(volleyball_metric_plot)

    else:
        plt.figure(figsize=(10, 6))
        for conf_teams, conf_name in zip(selected_conference_teams, selected_conferences):
            sns.kdeplot(data=conf_teams, x="+/- Hitting %", label=conf_name)
        plt.title("Average +/- Hitting Pct. Distribution(s) for Selected Conference(s)")
        plt.xlabel("Average +/- Hitting Pct.")
        plt.legend()
        st.pyplot(plt)

    with st.expander("See table"):
        st.dataframe(volleyball_df[["Team"] + volleyball_cols])

with soccer_tab:
    st.header("W Soccer Stats")

    with st.popover("Select conference(s)"):
        acc = st.checkbox("ACC", key="acc_soccer_checkbox")
        big_ten = st.checkbox("Big Ten", key="big_ten_soccer_checkbox")
        big_12 = st.checkbox("Big 12", key="big_12_soccer_checkbox")
        sec = st.checkbox("SEC", key="sec_soccer_checkbox")

    selected_conferences = []
    selected_conference_teams = []

    if acc:
        selected_conferences.append("ACC")
        selected_conference_teams.append(acc_teams)
    if big_ten:
        selected_conferences.append("Big Ten")
        selected_conference_teams.append(big_ten_teams)
    if big_12:
        selected_conferences.append("Big 12")
        selected_conference_teams.append(big_12_teams)
    if sec:
        selected_conferences.append("SEC")
        selected_conference_teams.append(sec_teams)

    soccer_cols = ["+/- GPG", "+/- GPG Z-Score"]
    soccer_df = filter_colleges_by_sport(all_stats_df, soccer_cols)
    soccer_df = filter_colleges_by_conferences(soccer_df, selected_conferences)
    soccer_df.sort_values("+/- GPG", ascending=False, inplace=True)
    soccer_df.reset_index(inplace=True)
    soccer_df.index = soccer_df.index + 1

    if len(selected_conferences) == 0:
        soccer_metric_plot = px.histogram(soccer_df, x="+/- GPG", title="Distribution of +/- GPG for All Teams")
        st.plotly_chart(soccer_metric_plot)

    else:
        plt.figure(figsize=(10, 6))
        for conf_teams, conf_name in zip(selected_conference_teams, selected_conferences):
            sns.kdeplot(data=conf_teams, x="+/- GPG", label=conf_name)
        plt.title("Average +/- GPG Distribution(s) for Selected Conference(s)")
        plt.xlabel("Average +/- GPG")
        plt.legend()
        st.pyplot(plt)

    with st.expander("See table"):
        st.dataframe(soccer_df[["Team"] + soccer_cols])