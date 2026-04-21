import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Badminton Stringing Analysis Dashboard",
    page_icon="🏸",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the most likely CSV from the data folder."""
    data_dir = Path("data")
    csv_files = sorted(data_dir.glob("*.csv"))

    if not csv_files:
        return pd.DataFrame()

    df = pd.read_csv(csv_files[-1])
    df.columns = [c.strip() for c in df.columns]

    # Flexible column normalization for common naming differences
    rename_map = {}
    for col in df.columns:
        lower = col.lower()
        if "gender" in lower:
            rename_map[col] = "Gender"
        elif "racket" in lower:
            rename_map[col] = "Racket"
        elif "string" in lower:
            rename_map[col] = "String"
        elif "tension" in lower:
            rename_map[col] = "Tension"
        elif "date" in lower:
            rename_map[col] = "Date"
        elif "player" in lower or "customer" in lower or "name" in lower:
            rename_map[col] = "Player"

    df = df.rename(columns=rename_map)

    if "Tension" in df.columns:
        df["Tension"] = pd.to_numeric(df["Tension"], errors="coerce")

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    for col in ["Gender", "Racket", "String", "Player"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


def required_columns_present(df: pd.DataFrame, columns: list[str]) -> bool:
    return all(col in df.columns for col in columns)


def iqr_outliers(series: pd.Series) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (series < lower) | (series > upper)


def metric_card(title: str, value: str, help_text: str = "") -> None:
    st.metric(label=title, value=value, help=help_text)


st.title("🏸 Badminton Stringing Analysis Dashboard")
st.caption(
    "Interactive dashboard for exploring racket preferences, string usage, tension patterns, and player trends."
)

# Sidebar
st.sidebar.header("Dashboard Filters")
df = load_data()

if df.empty:
    st.error("No CSV file was found in the data/ folder. Add your dataset to launch the dashboard.")
    st.stop()

available_genders = ["All"]
if "Gender" in df.columns:
    available_genders += sorted([g for g in df["Gender"].dropna().unique() if g and g != "nan"])
selected_gender = st.sidebar.selectbox("Gender", available_genders)

available_rackets = ["All"]
if "Racket" in df.columns:
    available_rackets += sorted([r for r in df["Racket"].dropna().unique() if r and r != "nan"])
selected_racket = st.sidebar.selectbox("Racket", available_rackets)

available_strings = ["All"]
if "String" in df.columns:
    available_strings += sorted([s for s in df["String"].dropna().unique() if s and s != "nan"])
selected_string = st.sidebar.selectbox("String", available_strings)

filtered_df = df.copy()
if selected_gender != "All" and "Gender" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
if selected_racket != "All" and "Racket" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Racket"] == selected_racket]
if selected_string != "All" and "String" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["String"] == selected_string]

if filtered_df.empty:
    st.warning("No rows match the current filter selection.")
    st.stop()

# Top metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Total Jobs", f"{len(filtered_df):,}")
with col2:
    if "Tension" in filtered_df.columns:
        metric_card("Average Tension", f"{filtered_df['Tension'].mean():.2f} lbs")
    else:
        metric_card("Average Tension", "N/A")
with col3:
    if "Racket" in filtered_df.columns:
        top_racket = filtered_df["Racket"].mode().iloc[0] if not filtered_df["Racket"].mode().empty else "N/A"
        metric_card("Most Popular Racket", top_racket)
    else:
        metric_card("Most Popular Racket", "N/A")
with col4:
    if "String" in filtered_df.columns:
        top_string = filtered_df["String"].mode().iloc[0] if not filtered_df["String"].mode().empty else "N/A"
        metric_card("Most Popular String", top_string)
    else:
        metric_card("Most Popular String", "N/A")

st.divider()

# Layout tabs
summary_tab, trends_tab, comparisons_tab, outliers_tab, data_tab = st.tabs(
    ["Overview", "Trends", "Comparisons", "Outliers", "Data Table"]
)

with summary_tab:
    left, right = st.columns((1.2, 1))

    with left:
        st.subheader("Most Popular Rackets")
        if "Racket" in filtered_df.columns:
            racket_counts = (
                filtered_df["Racket"]
                .value_counts()
                .reset_index()
            )
            racket_counts.columns = ["Racket", "Count"]
            fig_rackets = px.bar(
                racket_counts.head(10),
                x="Racket",
                y="Count",
                title="Top 10 Rackets",
            )
            fig_rackets.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_rackets, use_container_width=True)
        else:
            st.info("Racket column not found.")

    with right:
        st.subheader("Most Popular Strings")
        if "String" in filtered_df.columns:
            string_counts = (
                filtered_df["String"]
                .value_counts()
                .reset_index()
            )
            string_counts.columns = ["String", "Count"]
            fig_strings = px.bar(
                string_counts.head(10),
                x="String",
                y="Count",
                title="Top 10 Strings",
            )
            fig_strings.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_strings, use_container_width=True)
        else:
            st.info("String column not found.")

    st.subheader("Tension Distribution")
    if "Tension" in filtered_df.columns:
        fig_tension = px.histogram(
            filtered_df.dropna(subset=["Tension"]),
            x="Tension",
            nbins=20,
            title="String Tension Distribution",
        )
        st.plotly_chart(fig_tension, use_container_width=True)
    else:
        st.info("Tension column not found.")

    st.subheader("Insight Summary")
    insight_lines = []
    if "Racket" in filtered_df.columns and not filtered_df["Racket"].mode().empty:
        insight_lines.append(f"• Top racket: **{filtered_df['Racket'].mode().iloc[0]}**")
    if "String" in filtered_df.columns and not filtered_df["String"].mode().empty:
        insight_lines.append(f"• Top string: **{filtered_df['String'].mode().iloc[0]}**")
    if "Tension" in filtered_df.columns:
        insight_lines.append(f"• Average tension: **{filtered_df['Tension'].mean():.2f} lbs**")
        insight_lines.append(f"• Median tension: **{filtered_df['Tension'].median():.2f} lbs**")
    st.markdown("\n".join(insight_lines) if insight_lines else "No insights available.")

with trends_tab:
    st.subheader("Trend Exploration")
    if required_columns_present(filtered_df, ["Date", "Tension"]):
        trend_df = (
            filtered_df.dropna(subset=["Date", "Tension"])
            .sort_values("Date")
            .groupby(pd.Grouper(key="Date", freq="M"))["Tension"]
            .mean()
            .reset_index()
        )
        if not trend_df.empty:
            fig_trend = px.line(
                trend_df,
                x="Date",
                y="Tension",
                title="Average Tension Over Time",
                markers=True,
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("There is a Date column, but not enough valid dates to plot a trend.")
    else:
        st.info("Add a Date column to unlock time-based trend analysis.")

    if required_columns_present(filtered_df, ["Racket", "Tension"]):
        st.subheader("Average Tension by Racket")
        avg_racket_tension = (
            filtered_df.dropna(subset=["Racket", "Tension"])
            .groupby("Racket", as_index=False)["Tension"]
            .mean()
            .sort_values("Tension", ascending=False)
            .head(15)
        )
        fig_avg_racket = px.bar(
            avg_racket_tension,
            x="Racket",
            y="Tension",
            title="Average Tension by Racket",
        )
        fig_avg_racket.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig_avg_racket, use_container_width=True)

with comparisons_tab:
    st.subheader("Player Group Comparisons")

    if required_columns_present(filtered_df, ["Gender", "Tension"]):
        left, right = st.columns(2)
        with left:
            fig_gender_box = px.box(
                filtered_df.dropna(subset=["Gender", "Tension"]),
                x="Gender",
                y="Tension",
                title="Tension by Gender",
                points="outliers",
            )
            st.plotly_chart(fig_gender_box, use_container_width=True)
        with right:
            gender_avg = (
                filtered_df.dropna(subset=["Gender", "Tension"])
                .groupby("Gender", as_index=False)["Tension"]
                .mean()
            )
            fig_gender_avg = px.bar(
                gender_avg,
                x="Gender",
                y="Tension",
                title="Average Tension by Gender",
            )
            st.plotly_chart(fig_gender_avg, use_container_width=True)
    else:
        st.info("Gender and Tension columns are required for comparison views.")

    if required_columns_present(filtered_df, ["Gender", "Racket"]):
        st.subheader("Racket Preference by Gender")
        gender_racket = (
            filtered_df.groupby(["Gender", "Racket"])
            .size()
            .reset_index(name="Count")
        )
        fig_gender_racket = px.bar(
            gender_racket,
            x="Racket",
            y="Count",
            color="Gender",
            barmode="group",
            title="Racket Counts by Gender",
        )
        fig_gender_racket.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig_gender_racket, use_container_width=True)

with outliers_tab:
    st.subheader("Outlier Detection")
    if "Tension" in filtered_df.columns:
        outlier_df = filtered_df.dropna(subset=["Tension"]).copy()
        outlier_df["IsOutlier"] = iqr_outliers(outlier_df["Tension"])
        outlier_count = int(outlier_df["IsOutlier"].sum())

        st.metric("Detected Outliers", outlier_count)

        fig_outliers = px.strip(
            outlier_df,
            x="IsOutlier",
            y="Tension",
            hover_data=[c for c in ["Player", "Gender", "Racket", "String"] if c in outlier_df.columns],
            title="IQR-Based Tension Outliers",
        )
        st.plotly_chart(fig_outliers, use_container_width=True)

        st.subheader("Outlier Rows")
        st.dataframe(outlier_df[outlier_df["IsOutlier"]], use_container_width=True)
    else:
        st.info("Tension column not found.")

with data_tab:
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_stringing_data.csv",
        mime="text/csv",
    )

st.sidebar.divider()
st.sidebar.subheader("Portfolio Add-ons")
st.sidebar.markdown(
    "- Add a recommendation engine\n"
    "- Add player skill level\n"
    "- Add string durability tracking\n"
    "- Add date-based trend analysis\n"
    "- Deploy on Streamlit Community Cloud"
)
