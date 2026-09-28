from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# ============================================================
# CONFIGURATION
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "fitness.db"

st.set_page_config(
    page_title="Strava Fitness",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# COLOR THEMES  (pick from the sidebar)
# ============================================================
THEMES = {
    "Emerald Night": dict(
        dark=True, bg="#05130e", bg2="#0a2119", surface="rgba(52,211,153,.06)",
        border="rgba(52,211,153,.16)", text="#effaf5", muted="#8fb5a5",
        accent="#34d399", accent2="#86efac",
        colors=["#34d399", "#86efac", "#10b981", "#a3e635", "#14b8a6", "#059669"]),
    "Ocean Blue": dict(
        dark=True, bg="#06121f", bg2="#0a2036", surface="rgba(120,180,255,.07)",
        border="rgba(120,180,255,.16)", text="#eef5ff", muted="#8fa8c4",
        accent="#3b9eff", accent2="#22d3ee",
        colors=["#3b9eff", "#22d3ee", "#818cf8", "#34d399", "#fbbf24", "#f472b6"]),
    "Sunset Ember": dict(
        dark=True, bg="#160c0c", bg2="#241213", surface="rgba(255,190,150,.06)",
        border="rgba(255,190,150,.15)", text="#fff4ee", muted="#c3a294",
        accent="#ff7a45", accent2="#fbbf24",
        colors=["#ff7a45", "#fbbf24", "#f43f5e", "#fb7185", "#a3e635", "#38bdf8"]),
    "Royal Violet": dict(
        dark=True, bg="#0e0b1d", bg2="#1a1433", surface="rgba(190,170,255,.07)",
        border="rgba(190,170,255,.17)", text="#f5f2ff", muted="#a99fc9",
        accent="#a78bfa", accent2="#f0abfc",
        colors=["#a78bfa", "#f0abfc", "#60a5fa", "#34d399", "#fbbf24", "#fb7185"]),
    "Slate Mono": dict(
        dark=True, bg="#0f1115", bg2="#171a21", surface="rgba(255,255,255,.045)",
        border="rgba(255,255,255,.10)", text="#f1f2f4", muted="#9aa0ab",
        accent="#e5e7eb", accent2="#9ca3af",
        colors=["#e5e7eb", "#9ca3af", "#60a5fa", "#34d399", "#fbbf24", "#f87171"]),
}

st.sidebar.markdown("### 🏃 Strava Fitness")
st.sidebar.caption("Fitness analytics dashboard")

theme_name = st.sidebar.selectbox("🎨 Color theme", list(THEMES), key="theme")
T = THEMES[theme_name]

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "🚶 Activity", "😴 Sleep", "⏰ Hourly", "⚖️ Weight & BMI", "💡 Insights"],
)
chart_height = st.sidebar.slider("📐 Chart height", 380, 750, 500, step=20)
st.sidebar.markdown("---")
st.sidebar.caption("Python · Pandas · SQLite · Streamlit · Plotly")

# ============================================================
# CSS  (theme values injected as CSS variables)
# ============================================================
root_vars = f"""
:root {{
  --bg:{T['bg']}; --bg2:{T['bg2']}; --surface:{T['surface']}; --border:{T['border']};
  --text:{T['text']}; --muted:{T['muted']}; --accent:{T['accent']}; --accent2:{T['accent2']};
}}
"""

STATIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp { background: radial-gradient(1200px 600px at 85% -10%, var(--bg2), var(--bg)); color: var(--text); }
.stApp p, .stApp label, .stApp span, .stApp li, .stApp h1, .stApp h2, .stApp h3 { color: var(--text); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding: 2rem 3rem 3rem; max-width: 1450px; }

[data-testid="stSidebar"] { background: var(--bg2); border-right: 1px solid var(--border); }
[data-testid="stSidebar"] * { color: var(--text); }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 9px 12px; border-radius: 12px; transition: background .2s;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: var(--surface); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: var(--surface); box-shadow: inset 3px 0 0 var(--accent); font-weight: 700;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }

div[data-baseweb="select"] > div { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; }

.hero {
    padding: 30px 34px; border-radius: 24px; margin-bottom: 26px;
    background: linear-gradient(120deg, var(--surface), transparent 70%);
    border: 1px solid var(--border); position: relative; overflow: hidden;
}
.hero:before {
    content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px;
    background: linear-gradient(var(--accent), var(--accent2));
}
.hero-row { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.hero-title { font-size: 38px; font-weight: 800; letter-spacing: -1.2px; margin: 0; color: var(--text); }
.hero-sub { font-size: 15px; color: var(--muted); margin-top: 6px; }
.hero-icon {
    font-size: 40px; width: 74px; height: 74px; display: grid; place-items: center;
    border-radius: 22px; background: var(--surface); border: 1px solid var(--border);
}

.metric-card {
    padding: 20px 22px; border-radius: 20px; min-height: 128px;
    background: var(--surface); border: 1px solid var(--border);
    transition: border-color .2s, transform .2s;
}
.metric-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.metric-top { display: flex; align-items: center; gap: 10px; }
.metric-icon {
    font-size: 18px; width: 36px; height: 36px; display: grid; place-items: center;
    border-radius: 11px; background: var(--bg2); border: 1px solid var(--border);
}
.metric-label { font-size: 13px; font-weight: 600; color: var(--muted); }
.metric-value { font-size: 30px; font-weight: 800; letter-spacing: -.8px; margin-top: 12px; color: var(--text); }
.metric-note { font-size: 12px; color: var(--muted); margin-top: 2px; }

.section-title { font-size: 20px; font-weight: 700; margin: 30px 0 12px; color: var(--text); }

.insight {
    padding: 16px 20px; border-radius: 16px; margin-bottom: 10px;
    background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent);
}
.insight b { color: var(--accent); }
.insight-desc { color: var(--muted); display: block; margin-top: 3px; }

.warning {
    padding: 16px 20px; border-radius: 16px; margin: 6px 0 18px; line-height: 1.8;
    background: rgba(245,158,11,.10); border: 1px solid rgba(245,158,11,.30); color: var(--text);
}

[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }

.footer { margin-top: 40px; padding: 18px; text-align: center; color: var(--muted);
          font-size: 12px; border-top: 1px solid var(--border); }

@media (max-width: 800px) {
    .block-container { padding: 1rem; }
    .hero-title { font-size: 28px; }
    .hero-icon { display: none; }
}
"""
st.markdown(f"<style>{root_vars}{STATIC_CSS}</style>", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================
@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


@st.cache_data
def query(sql):
    return pd.read_sql_query(sql, get_connection())


# ============================================================
# HELPERS
# ============================================================
def metric_card(icon, label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_chart(fig, height=None):
    grid = "rgba(255,255,255,.07)" if T["dark"] else "rgba(15,30,60,.08)"
    fig.update_layout(
        template="plotly_dark" if T["dark"] else "plotly_white",
        colorway=T["colors"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=T["text"]),
        title=dict(font=dict(size=16)),
        margin=dict(l=20, r=20, t=60, b=50),
        height=height or chart_height,
        hoverlabel=dict(bgcolor=T["bg2"], font_color=T["text"]),
    )
    fig.update_xaxes(gridcolor=grid, zeroline=False, title_font=dict(size=12, color=T["muted"]))
    fig.update_yaxes(gridcolor=grid, zeroline=False, title_font=dict(size=12, color=T["muted"]))
    fig.update_traces(textposition="outside", cliponaxis=False,
                      textfont=dict(size=11, color=T["text"]), selector=dict(type="bar"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def hero(title, subtitle, icon):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-row">
                <div>
                    <div class="hero-title">{title}</div>
                    <div class="hero-sub">{subtitle}</div>
                </div>
                <div class="hero-icon">{icon}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


# ============================================================
# DATABASE CHECK
# ============================================================
if not DB_PATH.exists():
    st.error("SQLite database not found.")
    st.info("Run the following command first:")
    st.code("python src\\create_database.py")
    st.stop()

# ============================================================
# OVERVIEW
# ============================================================
if page == "🏠 Overview":
    hero("Strava Fitness", "Smart-device fitness intelligence at a glance", "🏃")

    overview = query("""
        SELECT COUNT(DISTINCT id) AS users,
               ROUND(AVG(totalsteps), 0) AS avg_steps,
               ROUND(AVG(calories), 0) AS avg_calories,
               ROUND(AVG(totaldistance), 2) AS avg_distance
        FROM daily_activity
    """)
    sleep = query("""
        SELECT ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep,
               COUNT(DISTINCT id) AS users
        FROM sleep
    """)
    o = overview.iloc[0]

    cols = st.columns(5)
    cards = [
        ("👥", "Users", f"{int(o['users']):,}", "Activity participants"),
        ("👟", "Avg steps", f"{int(o['avg_steps']):,}", "Per recorded day"),
        ("🔥", "Avg calories", f"{int(o['avg_calories']):,}", "Per recorded day"),
        ("📍", "Avg distance", f"{o['avg_distance']:.2f} km", "Per recorded day"),
        ("😴", "Avg sleep", f"{sleep.iloc[0]['avg_sleep']:.2f} hrs",
         f"{int(sleep.iloc[0]['users'])} users with data"),
    ]
    for col, c in zip(cols, cards):
        with col:
            metric_card(*c)

    section("Activity snapshot")

    levels = query("""
        SELECT activity_level, COUNT(*) AS user_count
        FROM (
            SELECT id,
                CASE
                    WHEN AVG(totalsteps) >= 10000 THEN 'Highly Active'
                    WHEN AVG(totalsteps) >= 7500 THEN 'Active'
                    WHEN AVG(totalsteps) >= 5000 THEN 'Moderately Active'
                    ELSE 'Less Active'
                END AS activity_level
            FROM daily_activity GROUP BY id
        )
        GROUP BY activity_level ORDER BY user_count DESC
    """)
    daily = query("""
        SELECT activitydate AS date, ROUND(AVG(totalsteps), 0) AS avg_steps
        FROM daily_activity GROUP BY activitydate ORDER BY activitydate
    """)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(levels, x="activity_level", y="user_count", text="user_count",
                     title="User activity segmentation",
                     labels={"activity_level": "Activity level", "user_count": "Number of users"})
        fig.update_traces(textposition="outside", marker_cornerradius=8)
        show_chart(fig)
    with c2:
        fig = px.area(daily, x="date", y="avg_steps", title="Daily average steps",
                      labels={"date": "Date", "avg_steps": "Average steps"})
        fig.update_traces(line=dict(width=2.5), opacity=0.85)
        top_day = daily.loc[daily["avg_steps"].idxmax()]
        fig.add_annotation(x=top_day["date"], y=top_day["avg_steps"], ay=-35, arrowhead=2,
                           text=f"Peak: {top_day['avg_steps']:,.0f}", font=dict(color=T["accent"]))
        show_chart(fig)

    c1, c2 = st.columns(2)
    with c1:
        relationship = query("SELECT totalsteps AS steps, calories FROM daily_activity")
        fig = px.scatter(relationship, x="steps", y="calories", title="Steps vs calories",
                         labels={"steps": "Daily steps", "calories": "Calories"}, opacity=0.6)
        show_chart(fig)
    with c2:
        intensity = query("""
            SELECT 'Very Active' AS activity_type, ROUND(AVG(veryactiveminutes), 1) AS minutes FROM daily_activity
            UNION ALL SELECT 'Fairly Active', ROUND(AVG(fairlyactiveminutes), 1) FROM daily_activity
            UNION ALL SELECT 'Lightly Active', ROUND(AVG(lightlyactiveminutes), 1) FROM daily_activity
            UNION ALL SELECT 'Sedentary', ROUND(AVG(sedentaryminutes), 1) FROM daily_activity
        """)
        fig = px.bar(intensity, x="activity_type", y="minutes", color="activity_type",
                     title="Average daily activity intensity", text_auto=".1f",
                     labels={"activity_type": "Activity type", "minutes": "Minutes per day"})
        fig.update_traces(marker_cornerradius=8)
        fig.update_layout(showlegend=False)
        show_chart(fig)

# ============================================================
# ACTIVITY
# ============================================================
elif page == "🚶 Activity":
    hero("Activity Intelligence", "Explore movement, calories and activity intensity", "🏃‍♂️")

    users = query("SELECT DISTINCT id FROM daily_activity ORDER BY id")
    selected_user = st.selectbox("Participant", ["All Users"] + users["id"].astype(str).tolist())

    # ids come from the database, so this cast keeps the query safe
    condition = "" if selected_user == "All Users" else f"WHERE id = {int(selected_user)}"

    activity = query(f"""
        SELECT id,
               ROUND(AVG(totalsteps), 0) AS avg_steps,
               ROUND(AVG(calories), 0) AS avg_calories,
               ROUND(AVG(veryactiveminutes), 1) AS very_active,
               ROUND(AVG(fairlyactiveminutes), 1) AS fairly_active,
               ROUND(AVG(lightlyactiveminutes), 1) AS lightly_active,
               ROUND(AVG(sedentaryminutes), 1) AS sedentary
        FROM daily_activity {condition}
        GROUP BY id ORDER BY avg_steps DESC
    """)

    c1, c2, c3 = st.columns(3)
    if selected_user == "All Users":
        with c1: metric_card("👥", "Participants", f"{len(activity):,}")
        with c2: metric_card("👟", "Average steps", f"{activity['avg_steps'].mean():,.0f}")
        with c3: metric_card("🔥", "Average calories", f"{activity['avg_calories'].mean():,.0f}")
    else:
        row = activity.iloc[0]
        with c1: metric_card("👟", "Average steps", f"{row['avg_steps']:,.0f}")
        with c2: metric_card("🔥", "Average calories", f"{row['avg_calories']:,.0f}")
        with c3: metric_card("🪑", "Sedentary minutes", f"{row['sedentary']:,.0f}")

    st.write("")
    top = activity.head(15).assign(id=lambda d: d["id"].astype(str))
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(top, x="id", y="avg_steps", title="Average steps by user", text_auto=",.0f",
                     labels={"id": "Participant ID", "avg_steps": "Average steps"})
        fig.update_traces(marker_cornerradius=6)
        fig.update_xaxes(type="category")
        show_chart(fig)
    with c2:
        fig = px.bar(top, x="id", y="avg_calories", title="Average calories by user", text_auto=",.0f",
                     labels={"id": "Participant ID", "avg_calories": "Average calories"})
        fig.update_traces(marker_cornerradius=6, marker_color=T["accent2"])
        fig.update_xaxes(type="category")
        show_chart(fig)

    intensity = activity[["very_active", "fairly_active", "lightly_active", "sedentary"]].mean().reset_index()
    intensity.columns = ["activity_type", "minutes"]
    fig = px.bar(intensity, x="activity_type", y="minutes", color="activity_type", title="Activity intensity",
             text_auto=".1f", labels={"activity_type": "Activity type", "minutes": "Minutes per day"})
    fig.update_traces(marker_cornerradius=8)
    fig.update_layout(showlegend=False)
    show_chart(fig)

    section("Activity records")
    st.dataframe(activity, use_container_width=True, hide_index=True)

# ============================================================
# SLEEP
# ============================================================
elif page == "😴 Sleep":
    hero("Sleep Intelligence", "Sleep duration and its relationship with movement", "😴")

    s = query("""
        SELECT COUNT(DISTINCT id) AS users,
               ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep,
               ROUND(AVG(TotalTimeInBed) / 60.0, 2) AS avg_bed
        FROM sleep
    """).iloc[0]

    c1, c2, c3 = st.columns(3)
    with c1: metric_card("👥", "Sleep users", int(s["users"]))
    with c2: metric_card("😴", "Average sleep", f"{s['avg_sleep']:.2f} hrs")
    with c3: metric_card("🛏️", "Time in bed", f"{s['avg_bed']:.2f} hrs")

    sleep_users = query("""
        SELECT id,
               ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS sleep_hours,
               ROUND(AVG(TotalTimeInBed) / 60.0, 2) AS bed_hours
        FROM sleep GROUP BY id ORDER BY sleep_hours DESC
    """)
    relationship = query("""
        SELECT s.id,
               ROUND(AVG(s.TotalMinutesAsleep) / 60.0, 2) AS sleep_hours,
               ROUND(AVG(a.TotalSteps), 0) AS avg_steps,
               ROUND(AVG(a.Calories), 0) AS avg_calories
        FROM sleep s
        JOIN daily_activity a
          ON s.id = a.id AND DATE(s.SleepDay) = DATE(a.ActivityDate)
        GROUP BY s.id
    """)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(sleep_users.assign(id=sleep_users["id"].astype(str)),
                     x="id", y="sleep_hours", title="Average sleep by user", text_auto=".1f",
                     labels={"id": "Participant ID", "sleep_hours": "Sleep (hours)"})
        fig.update_traces(marker_cornerradius=6)
        fig.update_xaxes(type="category")
        show_chart(fig)
    with c2:
        fig = px.scatter(relationship, x="sleep_hours", y="avg_steps",
                         hover_data=["id"], title="Sleep vs steps",
                         labels={"sleep_hours": "Average sleep (hours)", "avg_steps": "Average steps"})
        show_chart(fig)

    st.markdown(
        '<div class="insight">🔗 <b>Date-aligned analysis</b>'
        '<span class="insight-desc">Sleep and activity are matched using participant ID and date.</span></div>',
        unsafe_allow_html=True,
    )
    st.dataframe(sleep_users, use_container_width=True, hide_index=True)

# ============================================================
# HOURLY
# ============================================================
elif page == "⏰ Hourly":
    hero("Hourly Performance", "When movement and activity intensity peak", "⏱️")

    hourly_steps = query("""
        SELECT strftime('%H', ActivityHour) AS hour, ROUND(AVG(StepTotal), 0) AS avg_steps
        FROM hourly_steps GROUP BY hour ORDER BY hour
    """)
    hourly_intensity = query("""
        SELECT strftime('%H', ActivityHour) AS hour, ROUND(AVG(TotalIntensity), 2) AS avg_intensity
        FROM hourly_intensities GROUP BY hour ORDER BY hour
    """)
    hourly_count = query("SELECT COUNT(*) AS total_records FROM hourly_steps")
    peak = hourly_steps.loc[hourly_steps["avg_steps"].idxmax()]

    c1, c2, c3 = st.columns(3)
    with c1: metric_card("🕕", "Peak hour", f"{peak['hour']}:00")
    with c2: metric_card("👟", "Peak steps", f"{int(peak['avg_steps']):,}")
    with c3: metric_card("📊", "Hourly records", f"{int(hourly_count.iloc[0]['total_records']):,}")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.area(hourly_steps, x="hour", y="avg_steps", markers=True, title="Average steps by hour",
                      labels={"hour": "Hour of day", "avg_steps": "Average steps"})
        fig.add_annotation(x=peak["hour"], y=peak["avg_steps"], ay=-35, arrowhead=2,
                           text=f"Peak: {int(peak['avg_steps']):,} at {peak['hour']}:00",
                           font=dict(color=T["accent"]))
        show_chart(fig)
    with c2:
        fig = px.line(hourly_intensity, x="hour", y="avg_intensity", markers=True,
                      title="Average intensity by hour",
                      labels={"hour": "Hour of day", "avg_intensity": "Average intensity"})
        fig.update_traces(line=dict(color=T["accent2"], width=3), marker=dict(color=T["accent2"]))
        show_chart(fig)

    top_hours = hourly_steps.sort_values("avg_steps", ascending=False).head(10)
    fig = px.bar(top_hours, x="hour", y="avg_steps", text="avg_steps", title="Top 10 most active hours",
                 labels={"hour": "Hour of day", "avg_steps": "Average steps"})
    fig.update_traces(textposition="outside", marker_cornerradius=6)
    fig.update_xaxes(type="category")
    show_chart(fig)

# ============================================================
# WEIGHT & BMI
# ============================================================
elif page == "⚖️ Weight & BMI":
    hero("Weight & BMI", "Available body-composition records", "⚖️")

    w = query("""
        SELECT COUNT(DISTINCT id) AS users,
               ROUND(AVG(WeightKg), 2) AS avg_weight,
               ROUND(AVG(BMI), 2) AS avg_bmi
        FROM weight
    """).iloc[0]
    total_users = int(query("SELECT COUNT(DISTINCT id) AS n FROM daily_activity").iloc[0]["n"])

    c1, c2, c3 = st.columns(3)
    with c1: metric_card("👥", "Users", int(w["users"]), "Available weight data")
    with c2: metric_card("⚖️", "Average weight", f"{w['avg_weight']:.2f} kg")
    with c3: metric_card("📏", "Average BMI", f"{w['avg_bmi']:.2f}")

    st.markdown(
        f'<div class="warning">⚠️ Weight and BMI analysis covers only '
        f'<b>{int(w["users"])} of {total_users} participants</b>, so these figures '
        f'should not be treated as representative of the entire dataset.</div>',
        unsafe_allow_html=True,
    )

    weight = query("""
        SELECT id, ROUND(AVG(WeightKg), 2) AS avg_weight, ROUND(AVG(BMI), 2) AS avg_bmi
        FROM weight GROUP BY id ORDER BY avg_weight DESC
    """)
    wplot = weight.assign(id=weight["id"].astype(str))

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(wplot, x="id", y="avg_weight", title="Average weight by user", text_auto=".1f",
                     labels={"id": "Participant ID", "avg_weight": "Average weight (kg)"})
        fig.update_traces(marker_cornerradius=6)
        fig.update_xaxes(type="category")
        show_chart(fig)
    with c2:
        fig = px.bar(wplot, x="id", y="avg_bmi", title="Average BMI by user", text_auto=".1f",
                     labels={"id": "Participant ID", "avg_bmi": "Average BMI"})
        fig.update_traces(marker_cornerradius=6, marker_color=T["accent2"])
        fig.update_xaxes(type="category")
        show_chart(fig)

    st.dataframe(weight, use_container_width=True, hide_index=True)

# ============================================================
# INSIGHTS
# ============================================================
elif page == "💡 Insights":
    hero("Strava Fitness Insights", "Key findings from Python EDA and SQL analysis", "💡")

    insights = [
        ("👟", "Average movement", "Participants recorded an average of 7,638 steps per day."),
        ("🔥", "Steps and calories",
         "Daily steps and calories have a correlation of approximately 0.592. This indicates an association, not causation."),
        ("😴", "Sleep", "Average recorded sleep was 6.99 hours across 24 participants with sleep data."),
        ("🔗", "Sleep and movement",
         "The date-aligned sleep/steps analysis produced a correlation of approximately -0.066, indicating little linear association in this dataset."),
        ("⏰", "Peak period", "18:00 was the peak hour for average steps and activity intensity."),
        ("🏃", "Activity segmentation",
         "The 33 participants were classified into 7 Highly Active, 9 Active, 9 Moderately Active and 8 Less Active users."),
        ("⚖️", "Weight coverage",
         "Only 8 participants have weight records, so weight and BMI findings have limited coverage."),
        ("🪑", "Sedentary data",
         "Average recorded sedentary time was approximately 991 minutes per day. This should be interpreted as tracker-recorded sedentary time rather than automatically assuming confirmed waking inactivity."),
    ]

    left, right = st.columns(2)
    for i, (icon, title, desc) in enumerate(insights):
        with (left if i % 2 == 0 else right):
            st.markdown(
                f'<div class="insight">{icon} <b>{title}</b>'
                f'<span class="insight-desc">{desc}</span></div>',
                unsafe_allow_html=True,
            )

    section("Dataset limitations")
    st.markdown(
        """
        <div class="warning">
        • The dataset contains 33 participants and 940 daily activity records.<br>
        • Sleep information is available for 24 participants.<br>
        • Weight information is available for only 8 participants.<br>
        • Zero-step and zero-calorie records may represent days with limited or missing tracker activity.<br>
        • Correlations describe associations within this dataset and do not establish causation.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<div class="footer">Strava Fitness · Python, Pandas, SQLite, Streamlit and Plotly</div>',
    unsafe_allow_html=True,
)