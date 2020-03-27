"""
This example sends MIDI out. It sends NoteOn and then NoteOff with a random pitch bend.
"""

import time
import random
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import adafruit_ble_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend

# Use default HID descriptor
midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)
# advertisement.appearance = 961

ble = adafruit_ble.BLERadio()
if ble.connected:
    for c in ble.connections:
        c.disconnect()

midi = adafruit_midi.MIDI(midi_out=midi_service, out_channel=0)

print("advertising")
ble.start_advertising(advertisement)

while True:
    print("Waiting for connection")
    while not ble.connected:
        pass
    print("Connected")
    while ble.connected:
        midi.send(NoteOn(44, 120))  # G sharp 2nd octave
        time.sleep(0.25)
        a_pitch_bend = PitchBend(random.randint(0, 16383))
        midi.send(a_pitch_bend)
        time.sleep(0.25)
        # note how a list of messages can be used
        midi.send([NoteOff("G#2", 120), ControlChange(3, 44)])
        time.sleep(0.5)
    print("Disconnected")
    print()
    ble.start_advertising(advertisement)
