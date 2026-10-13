
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(
    page_title="Zenstar024 | Coffee Studio",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PREMIUM DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #38251d 0%, transparent 40%),
        radial-gradient(ellipse at 95% 30%, #20342a 0%, transparent 35%),
        #10120f;
    color: #f5eee3;
    font-family: 'DM Sans', sans-serif;
}
header[data-testid="stHeader"] {
    background: transparent;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f7e5c4 !important;
}
p, label, .stMarkdown {
    color: #e8dfd1;
}
.hero {
    background: linear-gradient(125deg, #36241b, #17251d 60%, #282017);
    border: 1px solid #796344;
    border-radius: 25px;
    padding: 34px 28px;
    text-align: center;
    margin-bottom: 25px;
    animation: fadeIn 1s ease-out;
    box-shadow: 0 15px 45px #0005;
}
.hero h1 {
    font-size: clamp(32px, 5vw, 56px);
    margin-bottom: 5px;
    background: linear-gradient(90deg, #fff0cc, #d7a75d, #fff0cc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #ddcbb2;
    font-size: 16px;
}
.coffee-card {
    background: linear-gradient(145deg, #28251f, #1b211c);
    border: 1px solid #514633;
    border-radius: 19px;
    padding: 20px;
    text-align: center;
    min-height: 175px;
    transition: transform .25s ease, border-color .25s ease;
    animation: fadeIn .7s ease-out;
}
.coffee-card:hover {
    transform: translateY(-5px);
    border-color: #e0b66c;
}
.coffee-emoji {
    font-size: 42px;
    margin-bottom: 8px;
}
.coffee-name {
    color: #f6e7cc;
    font-weight: 700;
    font-size: 18px;
}
.coffee-price {
    color: #dfb56f;
    font-size: 19px;
    font-weight: 700;
    margin-top: 8px;
}
.info-card {
    background: #201f1a;
    border: 1px solid #514633;
    border-radius: 15px;
    padding: 17px;
}
.stButton > button {
    background: linear-gradient(100deg, #d6ad6a, #f2d69d);
    color: #21180f !important;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 11px 18px;
    transition: transform .2s, box-shadow .2s;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 22px #d6ad6a55;
    border: none;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #211c17, #151a16);
    border-right: 1px solid #514633;
}
[data-testid="stMetric"] {
    background: #201f1a;
    border: 1px solid #514633;
    border-radius: 14px;
    padding: 15px;
}
[data-testid="stMetricValue"] {
    color: #e4bc79;
}
hr {
    border-color: #514633;
}
.small-note {
    color: #b9aa95;
    font-size: 12px;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(12px);}
    to {opacity: 1; transform: translateY(0);}
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- MENU ----------
MENU = {
    "Cappuccino": {"price": 320, "emoji": "☕", "desc": "Rich espresso with silky foam"},
    "Caramel Latte": {"price": 390, "emoji": "🍮", "desc": "Smooth latte with caramel sweetness"},
    "Americano": {"price": 250, "emoji": "🖤", "desc": "Bold espresso, clean finish"},
    "Mocha": {"price": 420, "emoji": "🍫", "desc": "Chocolate meets espresso"},
    "Vanilla Latte": {"price": 380, "emoji": "🤎", "desc": "Creamy vanilla coffee"},
    "Cold Coffee": {"price": 350, "emoji": "🧊", "desc": "Chilled, refreshing coffee"},
    "Espresso": {"price": 220, "emoji": "⚡", "desc": "A small cup with big character"},
    "Matcha Latte": {"price": 400, "emoji": "🍵", "desc": "Earthy matcha with creamy milk"},
}

# Demo prices in PKR; edit these to match your actual menu.
CURRENCY = "PKR"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "orders" not in st.session_state:
    st.session_state.orders = 0

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div style="font-size:48px;">☕ ✦ ☕</div>
    <h1>ZENSTAR024</h1>
    <p>COFFEE STUDIO · YOUR CUP, YOUR RULES</p>
    <div style="color:#d6ad6a;letter-spacing:3px;font-size:11px;">
        CRAFT YOUR PERFECT COFFEE
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## ☕ Coffee Studio")
    st.caption("Make every sip your own.")
    st.divider()

    st.markdown("### 🧾 Your Recipe")
    coffee = st.selectbox("Choose your coffee", list(MENU.keys()))
    size = st.selectbox(
        "Cup size",
        ["Small", "Regular", "Large"],
        index=1
    )
    milk = st.selectbox(
        "Milk preference",
        ["Whole milk", "Low-fat milk", "Oat milk",
         "Almond milk", "Soy milk", "No milk"]
    )
    sugar = st.select_slider(
        "Sugar level",
        options=["0%", "25%", "50%", "75%", "100%"],
        value="50%"
    )
    temperature = st.radio(
        "Temperature",
        ["Hot 🔥", "Iced 🧊"],
        horizontal=True
    )
    extras = st.multiselect(
        "Extras",
        ["Extra espresso (+80)", "Vanilla (+50)",
         "Caramel (+50)", "Whipped cream (+60)"]
    )
    quantity = st.number_input(
        "Quantity", min_value=1, max_value=20, value=1, step=1
    )

    size_extra = {"Small": 0, "Regular": 50, "Large": 100}
    extra_cost = sum(int(x.split("(+")[1].split(")")[0]) for x in extras)
    unit_price = MENU[coffee]["price"] + size_extra[size] + extra_cost
    line_total = unit_price * quantity

    st.divider()
    st.metric("Your total", f"{CURRENCY} {line_total:,}")

    if st.button("✨ Add to my order", use_container_width=True):
        st.session_state.cart.append({
            "Coffee": coffee,
            "Size": size,
            "Milk": milk,
            "Sugar": sugar,
            "Temperature": temperature,
            "Extras": ", ".join(extras) if extras else "None",
            "Quantity": int(quantity),
            "Unit price": unit_price,
            "Total": line_total
        })
        st.success(f"{coffee} added to your order!")

# ---------- MENU CARDS ----------
st.markdown("## ✨ Explore the Menu")
st.caption("Handpicked favourites for your coffee moment.")

columns = st.columns(4)
for i, (name, details) in enumerate(MENU.items()):
    with columns[i % 4]:
        st.markdown(f"""
        <div class="coffee-card">
            <div class="coffee-emoji">{details['emoji']}</div>
            <div class="coffee-name">{name}</div>
            <div style="color:#b9aa95;font-size:12px;margin-top:7px;">
                {details['desc']}
            </div>
            <div class="coffee-price">{CURRENCY} {details['price']:,}</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

st.divider()

# ---------- ORDER SUMMARY ----------
st.markdown("## 🛍️ Your Coffee Order")

if st.session_state.cart:
    cart_df = pd.DataFrame(st.session_state.cart)
    total_items = int(cart_df["Quantity"].sum())
    grand_total = int(cart_df["Total"].sum())

    m1, m2, m3 = st.columns(3)
    m1.metric("Different selections", len(cart_df))
    m2.metric("Total cups", total_items)
    m3.metric("Order total", f"{CURRENCY} {grand_total:,}")

    st.dataframe(cart_df, use_container_width=True, hide_index=True)

    left, right = st.columns(2)

    with left:
        csv_data = cart_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download order as CSV",
            data=csv_data,
            file_name="zenstar024_coffee_order.csv",
            mime="text/csv",
            use_container_width=True
        )

    with right:
        if st.button("🗑️ Clear my order", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

    st.info("This is a demo order builder. It does not send an order to Starbucks.")

else:
    st.markdown("""
    <div class="info-card" style="text-align:center;">
        <div style="font-size:42px;">☕</div>
        <h3>Your cup is waiting!</h3>
        <p style="color:#b9aa95;">
            Choose your coffee and customise it in the left panel.
            Press “Add to my order” to start building your collection.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.divider()
st.markdown("""
<div style="text-align:center;padding:15px;color:#b9aa95;">
    <div style="color:#d6ad6a;font-size:17px;">ZENSTAR024 · COFFEE STUDIO</div>
    <p class="small-note">
        Made for coffee lovers · Demo prices are illustrative · Not an official Starbucks app
    </p>
</div>
""", unsafe_allow_html=True)
