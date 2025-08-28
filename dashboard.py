# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Amazon Software Best-sellers 2025",
                   layout="wide")

# ------------- WIDGETS outside cache -------------
uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=['csv'])
countries_sel = st.sidebar.multiselect(
    "Country",
    options=['India','USA','Canada','Australia','Germany',
             'France','Italy','Spain','Japan'],
    default=['India','USA','Canada','Germany','Japan'])

price_range = st.sidebar.slider(
    "Price (numeric)",
    0.0, 500.0, (0.0, 500.0))

rating_range = st.sidebar.slider(
    "Rating",
    0.0, 5.0, (0.0, 5.0))

# ------------- CACHED pure data loader -------------
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
    else:
        df = pd.read_csv("Amazon_bestsellers_items_2025.csv")

    def parse_price(x):
        x = str(x).replace(',', '').replace('₹', '').replace('$', '').replace('€', '').replace('￥', '')
        try:
            return float(x)
        except:
            return np.nan

    df['price_num'] = df['product_price'].apply(parse_price)
    df['star_num'] = pd.to_numeric(df['product_star_rating'], errors='coerce')
    df['review_num'] = pd.to_numeric(df['product_num_ratings'], errors='coerce')
    df['country_name'] = df['country'].map({
        'IN': 'India', 'US': 'USA', 'CA': 'Canada', 'AU': 'Australia',
        'DE': 'Germany', 'FR': 'France', 'IT': 'Italy', 'ES': 'Spain', 'JP': 'Japan'
    })
    df['brand'] = df['product_title'].str.split().str[0].str.title()
    return df

df = load_data(uploaded)

# ------------- Filtering -------------
filtered = df[
    (df['country_name'].isin(countries_sel)) &
    (df['price_num'].between(*price_range)) &
    (df['star_num'].between(*rating_range))
]

# ------------- KPI cards -------------
st.title("🛒 Amazon Software Best-sellers – 2025")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("SKUs", f"{len(filtered):,}")
kpi2.metric("Avg Price", f"${filtered['price_num'].mean():,.2f}")
kpi3.metric("Avg Rating", f"{filtered['star_num'].mean():.2f} ⭐")
kpi4.metric("Reviews", f"{filtered['review_num'].sum():,.0f}")

# ------------- Charts -------------


st.subheader("💰 Price vs Rating")
scat_df = filtered.dropna(subset=['price_num', 'star_num', 'review_num'])
fig = px.scatter(
        scat_df, x='price_num', y='star_num',
        color='country_name', size='review_num',
        hover_name='product_title', log_x=True, height=450
    )
st.plotly_chart(fig, use_container_width=True)


st.subheader("📦 Price distribution")
box_df = filtered.dropna(subset=['price_num', 'country_name'])
if not box_df.empty:
        fig = px.box(
            box_df,
            x='price_num',
            y='country_name',
            color='country_name',
            log_x=True,
            height=450,
            points='outliers'
        )
        fig.update_layout(showlegend=False,
                          xaxis_title="Price",
                          yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

# ------------- Brand league -------------
st.subheader("🏆 Top Brands (≥500 reviews)")
brand_tbl = (filtered
             .groupby('brand')
             .agg(avg_rating=('star_num', 'mean'),
                  reviews=('review_num', 'sum'))
             .query('reviews >= 500')
             .sort_values('avg_rating', ascending=False)
             .head(20))
st.dataframe(brand_tbl, use_container_width=True)

# ------------- Raw table -------------
with st.expander("📋 Raw data"):
    cols = ['product_title', 'country_name', 'price_num', 'star_num', 'review_num']
    st.dataframe(filtered[cols].sort_values('review_num', ascending=False).reset_index(drop=True),
                 use_container_width=True)