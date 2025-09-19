import pyControl.utility as pc
from devices import Digital_input
from hardware_definition import final_valve, odor_A, odor_B

button = Digital_input('X17', rising_event='button_push', pull='up') # pyboard usr button.

pc.v.current_odor = "left"
pc.v.final_valve_flush_duration = 300

# State machine
states = ["wait", "set_odor", "deliver_odor", "final_valve_flush"]

events = ["button_push"]

initial_state = "wait"

def wait(event):
    if event == "entry":
        pc.v.current_odor = "left" if (pc.v.current_odor == "right") else "right"
    elif event == "button_push":
        pc.goto_state("set_odor")

def set_odor(event):
    if event == "entry":
        if pc.v.current_odor == "left":
            odor_A.on()
        elif pc.v.current_odor == "right":
            odor_B.on()
    elif event == "button_push":
        pc.goto_state("deliver_odor")

def deliver_odor(event):
    if event == "entry":
        final_valve.on()
    elif event == "button_push":
        pc.goto_state("final_valve_flush")
    elif event == "exit":
        odor_A.off()
        odor_B.off()

def final_valve_flush(event):
    if event == "entry":
        pc.timed_goto_state("wait", pc.v.final_valve_flush_duration)
    elif event == "exit":
        final_valve.off()

def run_end():
    odor_A.off()
    odor_B.off()
    final_valve.off()