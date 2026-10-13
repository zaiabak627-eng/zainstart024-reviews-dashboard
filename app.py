
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="ZENSTAR024 | Coffee Studio",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============== PREMIUM DESIGN ===============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 8% 0%, #493020 0%, transparent 35%),
        radial-gradient(ellipse at 95% 20%, #203d2b 0%, transparent 35%),
        linear-gradient(145deg, #0b100d, #151c16, #0b100d);
    color: #f6ead5;
    font-family: 'DM Sans', sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1500px; padding-top: 2rem; }
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f6e7cc !important;
}
.hero {
    text-align: center;
    padding: 45px 20px;
    border-radius: 28px;
    border: 1px solid #a88a54;
    background: linear-gradient(120deg, #39251a, #172c20 65%, #292219);
    box-shadow: 0 20px 60px #0008;
    animation: fadeIn 1s ease-out;
    margin-bottom: 25px;
}
.hero h1 {
    font-size: clamp(38px, 5vw, 68px);
    background: linear-gradient(90deg, #fff1cc, #d6a858, #fff1cc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 8px 0;
}
.hero p { color: #e3d1b2; letter-spacing: 2px; }
.eyebrow {
    color: #d9b574;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 4px;
}
.coffee-card {
    text-align: center;
    padding: 22px 15px;
    min-height: 225px;
    border-radius: 22px;
    border: 1px solid #5c5039;
    background: linear-gradient(145deg, #2a3026, #171e18);
    box-shadow: 0 12px 30px #0004;
    transition: transform .25s, border-color .25s, box-shadow .25s;
    animation: fadeIn .8s ease-out;
}
.coffee-card:hover {
    transform: translateY(-6px);
    border-color: #e1bd78;
    box-shadow: 0 18px 35px #0007;
}
.coffee-art {
    width: 78px;
    height: 78px;
    margin: 0 auto 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 25px;
    font-size: 40px;
    background: radial-gradient(circle at 30% 20%, #6a5033, #1b2b20);
    border: 1px solid #8a744d;
}
.coffee-name {
    font-size: 18px;
    font-weight: 700;
    color: #fff0d6;
}
.coffee-desc {
    font-size: 12px;
    color: #c3b9a7;
    min-height: 38px;
    margin-top: 8px;
}
.coffee-price {
    color: #e4bd77;
    font-size: 19px;
    font-weight: 700;
    margin-top: 10px;
}
.feature {
    padding: 17px;
    border: 1px solid #514b37;
    background: #1b241d;
    border-radius: 17px;
    margin-bottom: 20px;
}
.feature-title { color: #f2dfbd; font-weight: 700; }
.feature-sub { color: #b9b09e; font-size: 12px; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #211f18, #111912);
    border-right: 1px solid #514b37;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #242b22, #171e18);
    border: 1px solid #5b513b;
    border-radius: 16px;
    padding: 16px;
}
[data-testid="stMetricValue"] { color: #e4bd77; }
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(100deg, #c69a55, #f3dca9);
    color: #21180f !important;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    min-height: 43px;
    transition: transform .2s, box-shadow .2s;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px #d9b57455;
}
div[data-baseweb="select"] > div {
    background: #20271f;
    border-color: #514b37;
}
hr { border-color: #514b37; }
.small-note { color: #b9b09e; font-size: 11px; text-align: center; }
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =============== COFFEE MENU ===============
MENU = {
    "Cappuccino": {
        "price": 320, "emoji": "☕",
        "desc": "Velvety foam with a rich espresso heart."
    },
    "Caramel Latte": {
        "price": 390, "emoji": "🍮",
        "desc": "Smooth latte with golden caramel."
    },
    "Americano": {
        "price": 250, "emoji": "🖤",
        "desc": "Bold coffee with a clean finish."
    },
    "Mocha": {
        "price": 420, "emoji": "🍫",
        "desc": "Rich chocolate meets smooth espresso."
    },
    "Vanilla Latte": {
        "price": 380, "emoji": "🤎",
        "desc": "Creamy coffee with soft vanilla."
    },
    "Cold Coffee": {
        "price": 350, "emoji": "🧊",
        "desc": "Chilled, refreshing coffee."
    },
    "Espresso": {
        "price": 220, "emoji": "⚡",
        "desc": "A small cup with big character."
    },
    "Matcha Latte": {
        "price": 400, "emoji": "🍵",
        "desc": "Earthy matcha with creamy milk."
    }
}

CURRENCY = "PKR"
SIZE_EXTRA = {"Small": 0, "Regular": 50, "Large": 100}
EXTRA_PRICES = {
    "Extra espresso": 80,
    "Vanilla syrup": 50,
    "Caramel drizzle": 50,
    "Whipped cream": 60
}

if "cart" not in st.session_state:
    st.session_state.cart = []

# =============== HERO SECTION ===============
st.markdown("""
<div class="hero">
    <div style="font-size:48px">☕ ✦ ☕</div>
    <div class="eyebrow">SMALL-BATCH · SLOW MOMENTS · BIG FLAVOUR</div>
    <h1>ZENSTAR024</h1>
    <p>COFFEE STUDIO · YOUR CUP, YOUR RULES</p>
    <div style="color:#d9b574;letter-spacing:2px;font-size:12px">
        ✦ CRAFT YOUR SIGNATURE COFFEE ✦
    </div>
</div>
""", unsafe_allow_html=True)

# =============== FEATURES ===============
features = [
    ("✧", "Crafted with care", "Made around your taste"),
    ("◈", "Premium experience", "A little luxury in every sip"),
    ("☼", "Hot or iced", "Choose your coffee mood"),
    ("♡", "Made for you", "Customise every detail")
]

feature_cols = st.columns(4)

for col, item in zip(feature_cols, features):
    icon, title, subtitle = item
    with col:
        st.markdown(f"""
        <div class="feature">
            <div style="font-size:25px;color:#d9b574">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-sub">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

# =============== SIDEBAR CUSTOMISER ===============
with st.sidebar:
    st.markdown("## ☕ Coffee Studio")
    st.caption("Build your perfect cup.")
    st.divider()

    st.markdown("### 01 · Choose your coffee")
    coffee = st.selectbox("Coffee", list(MENU.keys()))
    size = st.selectbox(
        "Cup size", ["Small", "Regular", "Large"], index=1
    )

    st.markdown("### 02 · Make it yours")
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
        "Temperature", ["Hot 🔥", "Iced 🧊"],
        horizontal=True
    )
    extras = st.multiselect(
        "Extras", list(EXTRA_PRICES.keys())
    )
    quantity = st.number_input(
        "Quantity", min_value=1, max_value=20,
        value=1, step=1
    )

    extra_cost = sum(EXTRA_PRICES[x] for x in extras)
    unit_price = MENU[coffee]["price"] + SIZE_EXTRA[size] + extra_cost
    line_total = unit_price * int(quantity)

    st.divider()
    st.metric("Your cup total", f"{CURRENCY} {line_total:,}")

    if st.button("✦ Add to my order", use_container_width=True):
        st.session_state.cart.append({
            "Coffee": coffee,
            "Size": size,
            "Milk": milk,
            "Sugar": sugar,
            "Temperature": temperature,
            "Extras": ", ".join(extras) if extras else "None",
            "Quantity": int(quantity),
            "Unit price (PKR)": unit_price,
            "Total (PKR)": line_total
        })
        st.toast(f"{coffee} added to your order!", icon="☕")

# =============== MENU DISPLAY ===============
st.markdown(
    '<div class="eyebrow">THE SIGNATURE COLLECTION</div>',
    unsafe_allow_html=True
)
st.markdown("## Discover your next favourite")
st.caption("A curated menu for slow mornings and golden-hour breaks.")

menu_cols = st.columns(4)

for i, (name, details) in enumerate(MENU.items()):
    with menu_cols[i % 4]:
        st.markdown(f"""
        <div class="coffee-card">
            <div class="coffee-art">{details['emoji']}</div>
            <div class="coffee-name">{name}</div>
            <div class="coffee-desc">{details['desc']}</div>
            <div class="coffee-price">
                {CURRENCY} {details['price']:,}
                <span style="font-size:10px;color:#b9b09e"> / base</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

st.markdown("""
<div class="feature" style="text-align:center;padding:25px">
    <div class="eyebrow">THE ZENSTAR PROMISE</div>
    <div style="font-family:'Playfair Display',serif;
                font-size:25px;color:#f4e5cb;margin:10px 0">
        A slower moment. A better cup.
    </div>
    <div class="feature-sub">
        Choose your favourite, customise the details, and make it yours.
    </div>
</div>
""", unsafe_allow_html=True)

# =============== ORDER SUMMARY ===============
st.markdown(
    '<div class="eyebrow">YOUR SELECTION</div>',
    unsafe_allow_html=True
)
st.markdown("## 🛍️ Your coffee order")

if st.session_state.cart:
    cart_df = pd.DataFrame(st.session_state.cart)
    total_items = int(cart_df["Quantity"].sum())
    grand_total = int(cart_df["Total (PKR)"].sum())

    m1, m2, m3 = st.columns(3)
    m1.metric("Selections", len(cart_df))
    m2.metric("Total cups", total_items)
    m3.metric("Order total", f"{CURRENCY} {grand_total:,}")

    st.dataframe(
        cart_df, use_container_width=True, hide_index=True
    )

    left, right = st.columns(2)

    with left:
        st.download_button(
            "⬇ Download order summary",
            data=cart_df.to_csv(index=False).encode("utf-8"),
            file_name="zenstar024_order.csv",
            mime="text/csv",
            use_container_width=True
        )

    with right:
        if st.button("🗑️ Clear entire order", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

    st.caption(
        "Demo interface only: this does not send an order to a real café."
    )
else:
    st.markdown("""
    <div class="feature" style="text-align:center;padding:30px">
        <div style="font-size:45px">☕</div>
        <h3>Your next favourite is waiting.</h3>
        <p style="color:#b9b09e">
            Choose a coffee in the left panel, customise it,
            then press Add to my order.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =============== FOOTER ===============
st.divider()

st.markdown(f"""
<div style="text-align:center;padding:18px">
    <div style="font-family:'Playfair Display',serif;
                color:#d9b574;font-size:20px;letter-spacing:2px">
        ZENSTAR024 · COFFEE STUDIO
    </div>
    <div class="small-note">
        Made for coffee lovers · Demo prices in PKR ·
        Updated {datetime.now().strftime('%d %b %Y')}
    </div>
    <div class="small-note" style="margin-top:5px">
        Independent demo project — not an official Starbucks app.
    </div>
</div>
""", unsafe_allow_html=True)
