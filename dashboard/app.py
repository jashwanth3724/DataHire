import streamlit as st
import pandas as pd
import importlib
import importlib.util

HAVE_PLOTLY = importlib.util.find_spec("plotly") is not None

def get_px():
    if not HAVE_PLOTLY:
        return None
    return importlib.import_module("plotly.express")

def _safe_plot(fig):
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Plotly not installed — run `pip install plotly` to view charts.")
from pathlib import Path

st.markdown("""
<div class="hero">
    <h1>🚀 DataHire AI</h1>
    <p>
        India's AI-Powered Career Intelligence Platform
        <br>
        Analyze hiring trends, discover in-demand skills,
        find matching jobs, and plan your career path.
    </p>
</div>
""", unsafe_allow_html=True)
# ==========================

# CONFIG

# ==========================

st.set_page_config(
page_title="DataHire AI",
page_icon="📊",
layout="wide"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
}

/* KPI Cards */
.metric-card {
    background: linear-gradient(
        135deg,
        rgba(0,212,255,0.15),
        rgba(0,212,255,0.05)
    );
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    text-align: center;
    margin-bottom: 15px;
}

/* Hero Banner */
.hero {
    background: linear-gradient(
        135deg,
        #1f4037,
        #99f2c8
    );
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.hero h1 {
    color: white;
}

.hero p {
    color: white;
    font-size: 18px;
}

/* Job Cards */
.job-card {
    background-color: #1a1a1a;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid #2e2e2e;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1a1d29;
}

</style>
""", unsafe_allow_html=True)

# ==========================

# LOAD DATA

# ==========================

ROOT_DIR = Path(__file__).parent.parent

jobs_df = pd.read_csv(
ROOT_DIR / "data" / "processed" / "jobs_cleaned.csv"
)

skills_df = pd.read_csv(
ROOT_DIR / "data" / "processed" / "top_skills.csv"
)

# ==========================

# SIDEBAR

# ==========================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=100
)

st.sidebar.title("📊 DataHire AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Skill Analytics",
        "Job Search",
        "Career Advisor"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Live Job Market Intelligence Platform"
)

# NEW FILTER SECTION
st.sidebar.markdown("## 🔍 Filters")

selected_location = st.sidebar.selectbox(
    "📍 Location",
    ["All"] + sorted(
        jobs_df["location"].dropna().unique().tolist()
    )
)

selected_company = st.sidebar.selectbox(
    "🏢 Company",
    ["All"] + sorted(
        jobs_df["company"].dropna().unique().tolist()
    )
)

# ==========================

# DASHBOARD

# ==========================

if page == "Dashboard":

    st.title("📊 DataHire AI Dashboard")

    total_jobs = len(jobs_df)

    total_companies = jobs_df["company"].nunique()

    total_locations = jobs_df["location"].nunique()

    remote_jobs = 0

    if "remote" in jobs_df.columns:
        remote_jobs = jobs_df["remote"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💼 Jobs", total_jobs)
    c2.metric("🏢 Companies", total_companies)
    c3.metric("📍 Locations", total_locations)
    c4.metric("🏠 Remote Jobs", remote_jobs)
    st.markdown("## 📌 Market Insights")

    top_skill = skills_df.iloc[0]["Skill"]

    top_location = jobs_df["location"].value_counts().idxmax()

    top_company = jobs_df["company"].value_counts().idxmax()

    col1,col2,col3 = st.columns(3)

    with col1:
        st.success(f"🔥 Top Skill: {top_skill}")

    with col2:
        st.info(f"🌍 Top Location: {top_location}")

    with col3:
        st.warning(f"🏢 Top Company: {top_company}")

    st.markdown("---")
   

    st.subheader("🔥 Top Skills")

    px = get_px()
    if px:
        fig = px.bar(
            skills_df.head(10),
            x="Skill",
            y="Count",
            text="Count"
        )
    else:
        fig = None

    _safe_plot(fig)

    st.subheader("🔥 Trending Roles")

    role_df = (
        jobs_df["title"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    role_df.columns = ["Role","Count"]

    px = get_px()
    if px:
        fig = px.bar(
            role_df,
            x="Count",
            y="Role",
            orientation="h",
            color="Count"
        )
    else:
        fig = None

    _safe_plot(fig)

    st.subheader("🌍 Top Hiring Locations")

    location_df = (
        jobs_df["location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    location_df.columns = ["Location","Count"]

    px = get_px()
    if px:
        fig = px.bar(
            location_df,
            x="Count",
            y="Location",
            orientation="h",
            color="Count",
            title="Top Hiring Locations"
        )
    else:
        fig = None

    _safe_plot(fig)
# ==========================

# SKILL ANALYTICS

# ==========================

elif page == "Skill Analytics":

    st.title("📈 Skill Analytics")

    st.subheader(
        "Most Demanded Skills"
    )

    px = get_px()
    if px:
        fig = px.treemap(
            skills_df.head(20),
            path=["Skill"],
            values="Count"
        )
    else:
        fig = None

    _safe_plot(fig)

    st.subheader(
        "Top Skills Table"
    )

    st.dataframe(
        skills_df.head(20),
        use_container_width=True
    )

# ==========================

# JOB SEARCH

# ==========================

elif page == "Job Search":

    st.title("🔍 Job Search Engine")

    user_input = st.text_input(
        "Enter Skills",
        placeholder="Python, SQL, Power BI"
    )

    if user_input:

        user_skills = [
            x.strip().lower()
            for x in user_input.split(",")
        ]

        matches = []

        for _, row in jobs_df.iterrows():

            text = str(
                row.get("description", "")
            ).lower()

            score = 0

            for skill in user_skills:

                if skill in text:
                    score += 1

            if score > 0:

                matches.append({
                    "Job Title": row["title"],
                    "Company": row["company"],
                    "Location": row["location"],
                    "Match Score": round(
                        (score / len(user_skills))
                        * 100,
                        2
                    ),
                    "Apply Link": row.get("redirect_url", "")
                })

        if matches:

            result_df = pd.DataFrame(
                matches
            )

            result_df = result_df.sort_values(
                by="Match Score",
                ascending=False
            )

            st.success(
                f"{len(result_df)} Jobs Found"
            )

            for idx, row in result_df.head(15).iterrows():

                st.markdown(f"""
                <div class="job-card">

                <h3>💼 {row['Job Title']}</h3>

                <p>🏢 <b>{row['Company']}</b></p>

                <p>📍 {row['Location']}</p>

                <p>🎯 Match Score: <b>{row['Match Score']}%</b></p>

                </div>
                """, unsafe_allow_html=True)

                if row["Apply Link"]:

                    st.link_button(
                        "🚀 Apply Now",
                        row["Apply Link"],
                        key=f"apply_{idx}"
                    )

        else:

            st.warning(
                "No matching jobs found."
            )

# ==========================
# ==========================
# CAREER ADVISOR
# ==========================

elif page == "Career Advisor":

    st.title("🎯 Career Advisor")

    skills = st.text_input(
        "Enter Your Skills",
        placeholder="Python, SQL, Excel"
    )

    if skills:

        user_skills = [
            x.strip().lower()
            for x in skills.split(",")
        ]

        required = [
            "python",
            "sql",
            "excel",
            "power bi",
            "tableau",
            "statistics"
        ]

        missing = []

        for skill in required:

            if skill not in user_skills:
                missing.append(skill)

        score = (
            (
                len(required)
                - len(missing)
            )
            / len(required)
        ) * 100

        st.metric(
            "🎯 Data Analyst Readiness",
            f"{score:.0f}%"
        )

        st.progress(score / 100)

        if score > 80:

            st.success(
                "You are ready to apply for Data Analyst roles."
            )

        elif score > 60:

            st.warning(
                "You are close. Focus on the missing skills."
            )

        else:

            st.error(
                "You need more preparation."
            )

        st.subheader("📚 Missing Skills")

        if missing:

            for skill in missing:

                st.write(
                    f"❌ {skill.title()}"
                )

            st.markdown("---")

            st.subheader("🚀 Recommended Learning Path")

            for i, skill in enumerate(
                missing,
                start=1
            ):

                st.write(
                    f"{i}. Learn {skill.title()}"
                )

        else:

            st.success(
                "✅ You already have the core Data Analyst skills."
            )
