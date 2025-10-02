# SPDX-FileCopyrightText: 2025 spridget
# SPDX-License-Identifier: MIT

"""
This example acts as a BLE scanner for MIDI devices.
Specifically, it connects and pairs with a device running ble_midi_simple
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
from adafruit_ble_midi import MIDIService

# Use default HID descriptor
midi_service = adafruit_ble_midi.MIDIService()

ble = adafruit_ble.BLERadio()
if ble.connected:
    for c in ble.connections:
        c.disconnect()

midi = adafruit_midi.MIDI(midi_out=midi_service, midi_in=midi_service, out_channel=0)

while True:
    print("Waiting for connection to a MIDI device")
    for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=60):
        if MIDIService not in advertisement.services:
            continue
        ble.connect(advertisement)
        break

    if ble.connections:
        for connection in ble.connections:
            if connection.connected and not connection.paired:
                print("Connected; Pairing with the MIDI device")
                connection.pair()

        if connection.connected and connection.paired:
            print("Paired")
            midi_service = connection[MIDIService]
            midi = adafruit_midi.MIDI(midi_out=midi_service, midi_in=midi_service)

            while ble.connected:
                midi_in = midi.receive()
                while midi_in:
                    if not isinstance(midi_in, MIDIUnknownEvent):
                        print(time.monotonic(), midi_in)
                    midi_in = midi.receive()
            print("Disconnected")
            print()
