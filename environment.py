from utils import Phase

class SimulationContext:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimulationContext, cls).__new__(cls)
            cls._instance.message = []
            cls._instance.juror_to_speak = -1
            cls._instance.phase = None
            cls._instance.pooling_speakers_count = 0
            cls._instance.jury_size = 6
            cls._instance.ongoing_strategy = None
            cls._instance.is_own_witness = None
            cls._instance.witness_intention = None
            cls._instance.sequence_of_events = ''
        return cls._instance

    def set_message(self, message):
        self.message = message
    def append_message(self, message):
        self.message.append(message)

    def get_message(self):
        return self.message

    def set_phase(self, phase):
        self.phase = phase

    def get_phase(self):
        return self.phase
    
    def get_juror_to_speak(self):
        return self.juror_to_speak
    
    def set_juror_to_speak(self,juror_to_speak):
        self.juror_to_speak = juror_to_speak
    
    def get_pooling_speakers_count(self):
        return self.pooling_speakers_count
    
    def set_pooling_speakers_count(self, pooling_speakers_count):
        self.pooling_speakers_count = pooling_speakers_count
    
    def get_jury_size(self):
        return self.jury_size
    
    def set_ongoing_strategy(self, strategy):
        self.ongoing_strategy = strategy

    def get_ongoing_strategy(self):
        return self.ongoing_strategy
    
    def set_is_own_witness(self, flag):
        self.is_own_witness = flag
    
    def get_is_own_witness(self):
        return self.is_own_witness
    
    def set_witness_intention(self, intention):
        self.witness_intention = intention

    def get_witness_intention(self):
        return self.witness_intention
    
    def set_sequence_of_events(self, text):
        self.sequence_of_events = text

    def get_sequence_of_events(self):
        return self.sequence_of_events
# # Accessing the singleton instance
# context1 = SimulationContext()
# context2 = SimulationContext()

# context1.add_message("Message 1")
# print(context2.get_messages())  # Output: ["Message 1"]

class Context():
    def __init__(self,phase: Phase, jury_size):
        self.phase = phase
        self.juror_to_speak = None
        self.message = None
        self.pooling_speakers_count = None
        self.jury_size = jury_size
        self.ongoing_strategy = None


