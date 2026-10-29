import time
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

st.set_page_config(page_title="Virtual 8086 Stepper Motor Lab", page_icon="⚙️", layout="wide")

st.title("⚙️ Virtual 8086 Stepper Motor Laboratory")
st.caption("Educational simulation of 8086 stepper-motor interfacing — no physical hardware required.")

with st.sidebar:
    st.header("Motor controls")
    direction = st.radio("Rotation direction", ["Clockwise (CW)", "Anticlockwise (CCW)"])
    steps = st.slider("Number of steps", min_value=1, max_value=200, value=20, step=1)
    step_angle = st.selectbox("Motor step angle", [1.8, 7.5, 15.0, 90.0], index=2)
    delay_ms = st.slider("Simulation delay (ms per step)", 0, 250, 20, 10)
    run = st.button("▶ Run simulation", type="primary", use_container_width=True)
    reset = st.button("↺ Reset rotor", use_container_width=True)

if "position" not in st.session_state:
    st.session_state.position = 0.0
if "last_log" not in st.session_state:
    st.session_state.last_log = ["Ready. Choose a direction and run the simulation."]

if reset:
    st.session_state.position = 0.0
    st.session_state.last_log = ["Rotor position reset to 0°."]
    st.rerun()

# Correct the step-angle options in a user-friendly way.
# The 8086 lab program rotates the output pattern; this UI models the resulting rotor angle.
if run:
    sign = -1 if direction.startswith("Clockwise") else 1
    st.session_state.last_log = [
        f"Agent plan: rotate {direction.lower()} for {steps} step(s).",
        f"Pre-check: step angle = {step_angle:g}°, delay = {delay_ms} ms.",
        "Execution started: update phase pattern and rotor position."
    ]
    for i in range(steps):
        st.session_state.position = (st.session_state.position + sign * step_angle) % 360
        if delay_ms:
            time.sleep(delay_ms / 1000)
    st.session_state.last_log += [
        f"Execution complete: {steps} step(s) simulated.",
        f"Verification: final rotor position = {st.session_state.position:.1f}° (modulo 360°)."
    ]

left, right = st.columns([1.05, 1])
with left:
    st.subheader("Virtual stepper motor")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.axis("off")
    ax.add_patch(Circle((0, 0), 1.0, fill=False, linewidth=3))
    ax.add_patch(Circle((0, 0), 0.72, fill=False, linewidth=1.5))
    # Four stator poles
    for angle, label in [(0, "A"), (90, "B"), (180, "C"), (270, "D")]:
        ax.add_patch(Wedge((0, 0), 0.95, angle-16, angle+16, width=0.23, alpha=0.45))
        import math
        x, y = 1.13 * math.cos(math.radians(angle)), 1.13 * math.sin(math.radians(angle))
        ax.text(x, y, label, ha="center", va="center", fontsize=12, weight="bold")
    # Rotor arrow
    import math
    theta = math.radians(st.session_state.position)
    x, y = 0.65 * math.cos(theta), 0.65 * math.sin(theta)
    ax.annotate("", xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", linewidth=4))
    ax.add_patch(Circle((0, 0), 0.08, color="black"))
    ax.text(0, -1.28, f"Rotor position: {st.session_state.position:.1f}°",
            ha="center", va="center", fontsize=11)
    st.pyplot(fig, clear_figure=True)
    st.metric("Rotor position", f"{st.session_state.position:.1f}°")
    st.caption("Illustrative rotor animation/state. It is a software model, not an electrical simulation.")

with right:
    st.subheader("8086 ALP reference")
    tab1, tab2 = st.tabs(["Anticlockwise", "Clockwise"])
    anti = """; Anticlockwise rotation (based on supplied lab listing)
MOV AL, 80H
MOV DX, 0FFC6H
OUT DX, AL
MOV AL, 88H
MOV DX, 0FFC4H
OUT DX, AL
CALL DELAY
ROL AL, 1
JMP A1

DELAY:
MOV CX, 2000H
A2: LOOP A2
RET"""
    cw = """; Clockwise rotation (based on supplied lab listing)
MOV AL, 80H
MOV DX, 0FFC6H
OUT DX, AL
MOV AL, 88H
MOV DX, 0FFC4H
OUT DX, AL
CALL DELAY
ROR AL, 1
JMP A1

DELAY:
MOV CX, 2000H
A2: LOOP A2
RET"""
    with tab1:
        st.code(anti, language="asm")
    with tab2:
        st.code(cw, language="asm")
    st.warning("Port addresses and bit patterns are trainer-kit specific. Verify them against your kit manual before connecting hardware.")

st.divider()
st.subheader("Agentic workflow and execution log")
st.write("The simulated agent plans the movement, checks settings, executes the requested number of steps, and verifies the final rotor position.")
for item in st.session_state.last_log:
    st.write("• " + item)

st.subheader("How variable step-size works")
st.markdown("""
- **Number of steps** controls how many phase advances are simulated.
- **Motor step angle** controls the angular change assigned to each step.
- **Direction** selects the sign of the angular movement.
- The final displayed angle is wrapped into the range **0°–359.9°**.
""")
st.info("This is a teaching demo. The original assembly listing loops continuously; this simulator uses a finite step count so the result can be observed.")
