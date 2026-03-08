import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide", page_title="Bacterial Colony Simulator")

# ---------- CSS / STYLE ----------
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#e8f5e9,#e3f2fd,#f3e5f5);
}

h1{
text-align:center;
font-size:40px;
background: linear-gradient(90deg,#2e7d32,#1e88e5);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.stButton>button{
background:linear-gradient(90deg,#43a047,#66bb6a);
color:white;
font-size:18px;
padding:12px 25px;
border-radius:12px;
box-shadow:0 4px 12px rgba(0,0,0,0.2);
}

.stButton>button:hover{
transform:scale(1.08);
}

.element-container:hover{
transform:translateY(-3px);
transition:0.2s;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🦠Bacterial Colony Growth Simulator")

# ---------- CONTROLS ----------
st.markdown("### Simulation Controls")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    growth_rate = st.slider("Growth Rate",0.01,0.5,0.05)

with c2:
    colony_size = st.number_input("Initial Colony",50,1000,200)

with c3:
    rich_nutrients = st.checkbox("🌿 Rich Nutrients")

with c4:
    high_antibiotics = st.checkbox("💊 High Antibiotics")

with c5:
    mutation_rate = st.slider("Mutation Rate",0.0,0.2,0.02)

# ---------- CENTERED BUTTON ----------
b1,b2,b3 = st.columns([1,1,1])
with b2:
    run_sim = st.button("🚀 Run Simulation", use_container_width=True)

st.divider()

# ---------- DASHBOARD ----------
st.markdown("## 📊 Simulation Dashboard")

g1,g2 = st.columns(2)
g3,g4 = st.columns(2)

graph1 = g1.empty()
graph2 = g2.empty()
graph3 = g3.empty()
graph4 = g4.empty()

time_axis = np.arange(0,100)

# ---------- EMPTY GRAPHS ----------
fig,ax = plt.subplots(figsize=(4,3))
ax.set_title("Population Growth")
graph1.pyplot(fig)

fig,ax = plt.subplots(figsize=(4,3))
ax.set_title("Resistant Bacteria")
graph2.pyplot(fig)

fig,ax = plt.subplots(figsize=(4,3))
ax.set_title("Resistance vs Population")
graph3.pyplot(fig)

fig,ax = plt.subplots(figsize=(4,3))
ax.set_title("Petri Dish Distribution")
graph4.pyplot(fig)

# ---------- ANIMATION FUNCTION ----------
def animate_petri(population_size,resistant_ratio):

    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        placeholder = st.empty()

    for step in range(10):

        fig,ax = plt.subplots(figsize=(4,4))

        total = int(population_size*(step+1)/10)

        resistant = int(total*resistant_ratio)
        normal = total - resistant

        x = np.random.rand(total)
        y = np.random.rand(total)

        colors = ["green"]*normal + ["red"]*resistant

        ax.scatter(x,y,c=colors,alpha=0.7)

        ax.set_xlim(0,1)
        ax.set_ylim(0,1)

        ax.set_title(f"Colony Growth Step {step+1}")

        placeholder.pyplot(fig)

        time.sleep(0.35)

# ---------- SIMULATION ----------
if run_sim:

    nutrient_effect = 1.5 if rich_nutrients else 1
    antibiotic_effect = 0.4 if high_antibiotics else 1

    population = colony_size*np.exp(
        growth_rate*time_axis*nutrient_effect*antibiotic_effect
    )

    resistant = population*mutation_rate

    # GRAPH 1
    fig,ax = plt.subplots(figsize=(4,3))
    ax.plot(time_axis,population)
    ax.set_title("Population Growth")
    ax.set_xlabel("Time")
    ax.set_ylabel("Cells")
    graph1.pyplot(fig)

    # GRAPH 2
    fig,ax = plt.subplots(figsize=(4,3))
    ax.plot(time_axis,resistant)
    ax.set_title("Resistant Bacteria")
    graph2.pyplot(fig)

    # GRAPH 3
    fig,ax = plt.subplots(figsize=(4,3))
    ax.scatter(population,resistant)
    ax.set_title("Resistance vs Population")
    graph3.pyplot(fig)

    # GRAPH 4
    fig,ax = plt.subplots(figsize=(4,3))

    x=np.random.rand(200)
    y=np.random.rand(200)

    colors=["green"]*150+["red"]*50

    ax.scatter(x,y,c=colors)
    ax.set_title("Petri Dish Distribution")

    graph4.pyplot(fig)

    # ---------- METRICS ----------
    st.divider()
    st.subheader("📊 Simulation Metrics")

    m1,m2,m3 = st.columns(3)

    m1.metric("Final Population",int(population[-1]))
    m2.metric("Resistant Cells",int(resistant[-1]))

    resistance_percent = resistant[-1]/population[-1]*100
    m3.metric("Resistance %",f"{round(resistance_percent,2)}%")

    # ---------- ANIMATION ----------
    st.subheader("🧫 Animated Petri Dish Simulation")

    resistance_ratio = resistant[-1]/population[-1]

    animate_petri(colony_size,resistance_ratio)