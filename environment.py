from utils import Phase, StrategiesOwnWitnesses, StrategiesOpposingWitnesses

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
            cls._instance.witness_intention = None
            cls._instance.sequence_of_events = ''
            cls._instance.witness_speaking = None
            cls._instance.current_fact = None
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
    
    def set_witness_intention(self, intention):
        self.witness_intention = intention

    def get_witness_intention(self):
        return self.witness_intention
    
    def set_sequence_of_events(self, text):
        self.sequence_of_events = text

    def get_sequence_of_events(self):
        return self.sequence_of_events
    
    def set_witness_speaking(self, witness):
        self.witness_speaking = witness

    def get_witness_speaking(self):
        return self.witness_speaking
    
    def set_current_fact(self, fact):
        self.current_fact = fact

    def get_current_fact(self):
        return self.current_fact
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


