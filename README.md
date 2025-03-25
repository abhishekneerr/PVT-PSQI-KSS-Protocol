# Experiment Protocol Application

## Overview

This application is designed to run an experimental protocol using PyQt6. It features multiple screens including a welcome screen, demographic form, pre- and post-experiment questionnaires (PSQI and KSS), a PVT experiment screen, and an ending screen. The application uses a QStackedWidget to manage navigation between these different screens.

## Project Structure

- **src/main.py**: The main entry point of the application. It sets up the GUI, initializes the screens, and starts the event loop.
- **src/state.py**: Contains the state management functions (used to track changes across various screens).
- **screens/**: This directory holds the modules for each screen:
  - `welcome.py` - Welcome screen.
  - `demographic.py` - Demographic data form.
  - `psqi.py` - PSQI survey screens (before and after PVT).
  - `kss.py` - KSS survey screens (before and after PVT).
  - `pvt_instructions.py` - Instructions screen for the PVT test.
  - `pvt.py` - The PVT experimental screen.
  - `ending.py` - The final screen concluding the experiment.

## Prerequisites

- Python 3.7 or higher is recommended.
- PyQt6 (as specified in the requirements.txt).

## Installation

1. Clone the repository to your local machine.
2. Navigate to the repository directory.
3. (Optional) Create a virtual environment:
   
   ```python3 -m venv .venv```

4. Activate the virtual environment:
    ```source .venv/bin/activate```
5. Install the required dependencies:
    ```pip install -r requirements.txt```

## Running the Application
To launch the application, run the following command from the root directory of the project:
```python src/main.py``` or alternatively ```python -m src.main```

This will open the Experiment Protocol application window. 

For full-screen mode, you can uncomment the window.showFullScreen() line in src/main.py.


## Usage
Upon launching the application, you will be presented with the welcome screen. 
From there, you can navigate through the different screens using the provided buttons.


## Contributing


