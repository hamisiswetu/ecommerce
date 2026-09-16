import pandas as pd
import streamlit as st
#from sqlalchemy import create_engine
#import pymysql
import matplotlib.pyplot as plt

df = pd.read_csv("Ecommerce_daatset.csv")
#data = create_engine("mysql+pymysql://root:@localhost/ecommerce")
#df.to_sql(name="manunuzi", con=data, if_exists="replace", index=False)
#df_mysql = pd.read_sql("select * from manunuzi", con=data)

st.set_page_config(layout="wide")

# ------------------ BACKGROUND STYLING (LIGHT THEME) ------------------
st.markdown("""
<style>
/* Background ya dashboard nzima */
.stApp {
    background-color: #F5F7FA;
    color: #1a1a1a;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #e0e0e0;
}

/* Metric cards */
div[data-testid="stMetric"] {
    border: 1px solid #d9d9d9;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
    background-color: #FFFFFF;
}
div[data-testid="stMetricValue"] {
    color: #1f77b4;
}
div[data-testid="stMetricLabel"] {
    color: #444444;
}

/* Expander styling */
div[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border-radius: 10px;
    border: 1px solid #d9d9d9;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a;
}
</style>
""", unsafe_allow_html=True)

st.subheader("E-commerce Dashboard")

st.sidebar.subheader("Filter data")
category = st.sidebar.multiselect(
    "Select category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)
brand = st.sidebar.multiselect(
    "Select brand",
    options=df["Brand"].unique(),
    default=df["Brand"].unique()
)
user_age = st.sidebar.slider(
    "Select user_age",
    int(df["User_Age"].min()),
    int(df["User_Age"].max()),
    (int(df["User_Age"].min()), int(df["User_Age"].max()))
)
user_gender = st.sidebar.multiselect(
    "Select user_gender",
    options=df["User_Gender"].unique(),
    default=df["User_Gender"].unique()
)
user_location = st.sidebar.multiselect(
    "Select user_location",
    options=df["User_Location"].unique(),
    default=df["User_Location"].unique()
)

selection = df[
    (df["Category"].isin(category)) & (df["Brand"].isin(brand)) &
    (df_mysql["User_Age"] >= user_age[0]) & (df["User_Age"] <= user_age[1]) &
    (df["User_Gender"].isin(user_gender)) & (df["User_Location"].isin(user_location))
]


def hesabu(selection):
    return {
        "total": selection["Product_Price"].sum(),
        "Average": selection["Product_Price"].mean(),
        "Maximum": selection["Product_Price"].max(),
        "Minimum": selection["Product_Price"].min()
    }


matrics = hesabu(selection)


def show_matrics(matrics):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Price", f"{matrics['total']:,.0f}")
    c2.metric("Average Price", f"{matrics['Average']:,.0f}")
    c3.metric("Maximum Price", f"{matrics['Maximum']:,.0f}")
    c4.metric("Minimum Price", f"{matrics['Minimum']:,.0f}")


show_matrics(matrics)

# ------------------ EXPANDER: DATASET + COLUMN SELECTOR ------------------
with st.expander("📂 Angalia Dataseti Kamili (View Full Dataset)"):
    selected_columns = st.multiselect(
        "Chagua columns unazotaka kuona",
        options=selection.columns.tolist(),
        default=selection.columns.tolist()
    )

    if selected_columns:
        st.dataframe(selection[selected_columns], use_container_width=True)
    else:
        st.warning("Tafadhali chagua angalau column moja ili kuona data.")

    st.markdown(f"**Idadi ya rekodi (rows):** {selection.shape[0]}  |  **Idadi ya columns zilizochaguliwa:** {len(selected_columns)}")

# ------------------ STYLING YA CHARTS ------------------
plt.style.use("seaborn-v0_8-whitegrid")
colors = plt.cm.Set2.colors

st.markdown("### Visualizations")
c1, c2 = st.columns(2)

# PIE CHART
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    counts = selection["Category"].value_counts()

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 9, "color": "#1a1a1a"}
    )
    for at in autotexts:
        at.set_color("#1a1a1a")
        at.set_fontweight("bold")

    ax.set_title("Products by Category", fontsize=13, fontweight="bold", color="#1a1a1a")
    fig.patch.set_alpha(0)
    fig.tight_layout()
    st.pyplot(fig, transparent=True)

# BAR CHART
with c2:
    fig, ax = plt.subplots(figsize=(5, 5))
    counts_sorted = selection["Category"].value_counts().sort_values()

    bars = ax.barh(
        counts_sorted.index,
        counts_sorted.values,
        color=colors[:len(counts_sorted)],
        edgecolor="white"
    )

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f"{int(width)}", va="center", fontsize=9, color="#1a1a1a")

    ax.set_title("Products by Category", fontsize=13, fontweight="bold", color="#1a1a1a")
    ax.set_xlabel("Number of Products", color="#1a1a1a")
    ax.set_ylabel("")
    ax.tick_params(colors="#1a1a1a")
    fig.patch.set_alpha(0)
    fig.tight_layout()
    st.pyplot(fig, transparent=True)
