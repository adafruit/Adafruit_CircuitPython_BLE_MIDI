# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example acts as a keyboard to peer devices.
"""

import time

import adafruit_ble
import adafruit_midi
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

# These import auto-register the message type with the MIDI machinery.
from adafruit_midi.control_change import ControlChange
from adafruit_midi.midi_message import MIDIUnknownEvent
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend

import adafruit_ble_midi

# Use default HID descriptor
midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)

ble = adafruit_ble.BLERadio()
if ble.connected:
    for c in ble.connections:
        c.disconnect()

midi = adafruit_midi.MIDI(midi_out=midi_service, midi_in=midi_service, out_channel=0)

print("advertising")
ble.start_advertising(advertisement)

while True:
    print("Waiting for connection")
    while not ble.connected:
        pass
    print("Connected")
    while ble.connected:
        midi_in = midi.receive()
        while midi_in:
            if not isinstance(midi_in, MIDIUnknownEvent):
                print(time.monotonic(), midi_in)
            midi_in = midi.receive()
    print("Disconnected")
    print()
    ble.start_advertising(advertisement)
