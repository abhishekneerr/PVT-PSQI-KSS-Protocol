import sys
import os
# Get the absolute path of the project root (one level up from src/) to find screens and utils directories
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)  

# import necessary modules
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from screens.welcome import create_welcome_screen
from screens.demographic import create_demographic_form
from screens.psqi import create_psqi_beforePVT_screen, create_psqi_afterPVT_screen
from screens.kss import create_kss_beforePVT_screen, create_kss_afterPVT_screen
from screens.pvt_instructions import create_pvt_instructions_screen
from screens.pvt import create_experiment_PVT_screen
from screens.ending import create_ending_screen


from src.state import state_manager



def create_main_window():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Experiment Protocol")
    # window.setMinimumSize(1000, 800)
    window.showFullScreen()     #full screen mode
    
    stack = QStackedWidget()
    stack.addWidget(create_welcome_screen(stack))
    stack.addWidget(create_demographic_form(stack))
    stack.addWidget(create_psqi_beforePVT_screen(stack))
    stack.addWidget(create_kss_beforePVT_screen(stack))
    stack.addWidget(create_pvt_instructions_screen(stack))
    stack.addWidget(create_experiment_PVT_screen(stack))
    stack.addWidget(create_kss_afterPVT_screen(stack))
    stack.addWidget(create_psqi_afterPVT_screen(stack))
    stack.addWidget(create_ending_screen(stack))

    layout = QVBoxLayout()
    layout.addWidget(stack)
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    create_main_window()
