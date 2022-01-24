Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ble_midi/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ble_midi/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_BLE_MIDI/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_BLE_MIDI/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

BLE MIDI service for CircuitPython


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ble_midi/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ble-midi

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ble-midi

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-ble-midi

Usage Example
=============

.. code-block:: python

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

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ble_midi/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_BLE_MIDI/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
