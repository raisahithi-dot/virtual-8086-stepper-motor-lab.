# Virtual 8086 Stepper Motor Laboratory

A small interactive Streamlit project for demonstrating stepper-motor interfacing concepts from an 8086 microprocessor lab.

## Features

- Simulated rotor position and rotation direction
- Selectable clockwise or anticlockwise direction
- Variable number of steps and step angle
- Adjustable simulation delay
- 8086 ALP reference tabs for both directions
- Execution log showing plan, execution, and verification
- Runs locally or can be deployed from GitHub

> **Important:** This is a software simulation. It does not control real hardware. Port addresses and output patterns are trainer-kit specific; verify them against your hardware manual before connecting a motor.

## Run on your computer

Requires Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment:

- Windows: `.venv\\Scripts\\activate`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`).

## Deploy from GitHub using Streamlit Community Cloud

1. Create a new repository on GitHub, for example `virtual-8086-stepper-motor-lab`.
2. Upload `app.py`, `requirements.txt`, and `README.md` from this project.
3. Open Streamlit Community Cloud and connect your GitHub account.
4. Select the repository, branch (usually `main`), and main file path `app.py`.
5. Deploy.

## Using the simulator

1. Select **Clockwise (CW)** or **Anticlockwise (CCW)**.
2. Set the number of steps, motor step angle, and delay.
3. Click **Run simulation**.
4. Observe the rotor position and the execution log.
5. Use **Reset rotor** to return to 0°.

## Project structure

```text
virtual-8086-stepper-motor-lab/
├── app.py
├── requirements.txt
└── README.md
```

## Learning objectives

- Understand the idea of sequencing output patterns to rotate a stepper motor.
- Compare clockwise and anticlockwise operation.
- Observe how step count and step angle affect final rotor position.
- Relate a software simulation to the 8086 assembly-language lab.

## Note about the supplied ALP

The assembly snippets in the app preserve the main instructions from the supplied lab listing for learning/reference. The listing appears to use trainer-specific I/O ports and an indefinitely repeated loop. Actual step-size control and motor stepping sequence depend on the interface circuit and trainer-kit documentation.
