import streamlit as st
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(layout="wide", page_title="Football Tactical Board")

# ---------- SESSION STATE ----------
for key, default in {
    "players": [],
    "arrows": [],
    "zones": [],
    "home_name": "HOME",
    "away_name": "AWAY",
    "home_score": 0,
    "away_score": 0,
    "minute": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚽ Tactical Board")

st.sidebar.subheader("Match Info")
st.session_state.home_name = st.sidebar.text_input("Home Team", st.session_state.home_name)
st.session_state.away_name = st.sidebar.text_input("Away Team", st.session_state.away_name)
st.session_state.home_score = st.sidebar.number_input("Home Score", 0, 20, st.session_state.home_score)
st.session_state.away_score = st.sidebar.number_input("Away Score", 0, 20, st.session_state.away_score)
st.session_state.minute = st.sidebar.number_input("Minute", 0, 130, st.session_state.minute)

st.sidebar.divider()

mode = st.sidebar.selectbox("Mode", ["Player", "Arrow", "Zone"])

# ---------- PLAYER ----------
if mode == "Player":
    team = st.sidebar.selectbox("Team", ["Home", "Away"])
    number = st.sidebar.number_input("Player Number", 1, 99, 1)

    x = st.sidebar.slider("X position", 0, 100, 50)
    y = st.sidebar.slider("Y position", 0, 100, 50)

    if st.sidebar.button("➕ Add Player"):
        st.session_state.players.append({
            "x": x,
            "y": y,
            "team": team,
            "number": number
        })

# ---------- ARROW ----------
if mode == "Arrow":
    st.sidebar.subheader("Arrow")
    x1 = st.sidebar.slider("Start X", 0, 100, 40)
    y1 = st.sidebar.slider("Start Y", 0, 100, 50)
    x2 = st.sidebar.slider("End X", 0, 100, 70)
    y2 = st.sidebar.slider("End Y", 0, 100, 50)

    if st.sidebar.button("➕ Add Arrow"):
        st.session_state.arrows.append((x1, y1, x2, y2))

# ---------- ZONE ----------
if mode == "Zone":
    st.sidebar.subheader("Zone")
    zx = st.sidebar.slider("Center X", 0, 100, 50)
    zy = st.sidebar.slider("Center Y", 0, 100, 50)
    w = st.sidebar.slider("Width", 5, 50, 20)
    h = st.sidebar.slider("Height", 5, 50, 20)

    if st.sidebar.button("➕ Add Zone"):
        st.session_state.zones.append((zx, zy, w, h))

# ---------- CLEAR ----------
if st.sidebar.button("🧹 Clear Board"):
    st.session_state.players = []
    st.session_state.arrows = []
    st.session_state.zones = []

# ---------------- DRAW PITCH ----------------
fig, ax = plt.subplots(figsize=(18, 10))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Grass
ax.add_patch(plt.Rectangle((0, 0), 100, 100, color="#1f8f3a"))

# Stripes
for i in range(0, 100, 10):
    ax.add_patch(plt.Rectangle((i, 0), 5, 100, color="#1b7f34"))

# Lines
ax.add_patch(plt.Rectangle((2, 2), 96, 96, fill=False, edgecolor="white", linewidth=2))
ax.plot([50, 50], [2, 98], color="white", linewidth=2)
ax.add_patch(plt.Circle((50, 50), 9, fill=False, edgecolor="white", linewidth=2))

# Zones
for zx, zy, w, h in st.session_state.zones:
    ax.add_patch(plt.Rectangle(
        (zx - w/2, zy - h/2),
        w, h,
        color="yellow", alpha=0.35
    ))

# Arrows
for x1, y1, x2, y2 in st.session_state.arrows:
    ax.arrow(
        x1, y1, x2 - x1, y2 - y1,
        width=0.6, head_width=3, head_length=3,
        color="red", length_includes_head=True
    )

# Players
for p in st.session_state.players:
    color = "#3b82f6" if p["team"] == "Home" else "#ef4444"
    ax.scatter(p["x"], p["y"], s=700, color=color,
               edgecolors="white", zorder=5)
    ax.text(p["x"], p["y"], str(p["number"]),
            color="white", ha="center", va="center",
            fontweight="bold", fontsize=10)

# TV Overlay
overlay = f"{st.session_state.home_name} {st.session_state.home_score} - {st.session_state.away_score} {st.session_state.away_name}   {st.session_state.minute}'"
ax.text(2, 98, overlay,
        color="white", fontsize=16, fontweight="bold",
        bbox=dict(facecolor="black", alpha=0.85))

st.pyplot(fig)