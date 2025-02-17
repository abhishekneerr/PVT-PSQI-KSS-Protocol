import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



class StateManager:
    def __init__(self):
        self.participant_id = ""

    def set_participant_id(self, participant_id):
        self.participant_id = participant_id
        # logging.debug(f"Participant ID set to {participant_id}")

    def get_participant_id(self):
        # logging.debug(f"Getting participant ID: {self.participant_id}")
        return self.participant_id


# Create a single global instance of StateManager
state_manager = StateManager()


