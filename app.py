import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #E3F2FD;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Movie Trailer popularity", layout="wide")

# ---------------- TITLE & ABOUT ----------------
st.title("🎬 Movie Trailer Popularity Model")
st.markdown(
    """
This project predicts how a movie trailer spreads among viewers using an **SIR-based model**.

- **S (Susceptible)** → People who have not watched the trailer  
- **I (Active)** → People who are watching and sharing  
- **R (Dropped)** → People who stopped sharing  

👉 Enter values in the sidebar and click **Run Simulation** to see results.
"""
)

# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("Input Parameters")

N = st.sidebar.number_input("Peak Active", 1000, 1000000, 100000)
initial_I = st.sidebar.number_input("peak day", 1, 10000, 100)
beta = st.sidebar.slider("Sharing Rate (beta)", 0.01, 1.0, 0.3)
gamma = st.sidebar.slider("Drop Rate (gamma)", 0.01, 1.0, 0.1)
decay = st.sidebar.slider("Decay Rate", 0.0, 0.1, 0.01)
days = st.sidebar.slider("Days", 10, 180, 60)

# ---------------- BUTTONS ----------------
run = st.sidebar.button("Run Simulation")
reset = st.sidebar.button("Reset")

if reset:
    st.rerun()

# ---------------- SIMULATION FUNCTION ----------------
def simulate(N, initial_I, beta, gamma, decay, days):
    S = N - initial_I
    I = initial_I
    R = 0

    S_list, I_list, R_list = [], [], []

    for t in range(days):
        new_viewers = beta * S * I / N
        new_viewers *= np.exp(-decay * t)
        dropped = gamma * I

        S -= new_viewers
        I += new_viewers - dropped
        R += dropped

        S_list.append(S)
        I_list.append(I)
        R_list.append(R)

    peak_viewers = max(I_list)
    peak_day = I_list.index(peak_viewers) + 1

    return S_list, I_list, R_list, peak_viewers, peak_day

# ---------------- SHOW OUTPUT ONLY AFTER CLICK ----------------
if run:
    S_list, I_list, R_list, peak_viewers, peak_day = simulate(
        N, initial_I, beta, gamma, decay, days
    )

    st.markdown("---")
    st.subheader("📊 Simulation Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Active Viewers", int(peak_viewers))
    col2.metric("Peak Day", peak_day)
    col3.metric("Final Dropped Viewers", int(R_list[-1]))

    # Graph
    fig, ax = plt.subplots()
    ax.plot(S_list, label="Susceptible")
    ax.plot(I_list, label="Active")
    ax.plot(R_list, label="Dropped")
    ax.set_xlabel("Days")
    ax.set_ylabel("People")
    ax.set_title("Virality Trend")
    ax.legend()

    st.pyplot(fig)

    # Interpretation
    st.subheader("📌 Interpretation")
    st.write(
        f"""
The trailer becomes most viral on **Day {peak_day}** with approximately **{int(peak_viewers)} active viewers**.
After this point, the number of active sharers decreases due to reduced interest and drop rate.
"""
    )
