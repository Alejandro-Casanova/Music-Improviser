import os
import sys
import time

from mingus.core import scales, meter, chords, progressions, keys
from mingus.containers import Note, NoteContainer, Bar, Track, instrument
from mingus.midi import fluidsynth
from random import randint, random, choice
from custom_functions import custom_play_bars, format_chords, relative_modulation, parallel_modulation, \
    step_modulation, is_mayor  # My custom functions

# Defines Macros (Channels and Volumes)
CHORD_VOLUME = 65
MELODY_VOLUME = 100
PERC_VOLUME = 127

CHORD_CHANNEL = 1
MELODY_CHANNEL = 2
PERC_CHANNEL = 9

fluidsynth.init("GeneralUserGSv1.471.sf2", "pulseaudio")

# Chord Progressions Played and Scales
key_play = 'C'
minor_chords = ["Im", "IIdim", "III", "IVm", "Vm", "VI", "VII"]
mayor_chords = ["I", "IIm", "IIIm", "IV", "V", "VIm", "VIIdim"]
# prog = progressions.to_chords(["I", "V", "vi", "IV"], key_play)  # Sharp 2nd??
# prog = progressions.to_chords(["I", "II", "III", "V", "vi", "IV"], key_play)  # Sharp 2nd??
#prog_mayor = progressions.to_chords(mayor_chords, 'C')  # Sharp 2nd??
#prog_minor = progressions.to_chords(minor_chords, 'c')  # Sharp 2nd??
#prog_all = prog_mayor + prog_minor

prog_play = progressions.to_chords([minor_chords, mayor_chords][is_mayor(key_play)], key_play)
prog_play = format_chords(prog_play, CHORD_VOLUME, CHORD_CHANNEL)
#prog_mayor = format_chords(prog_mayor, CHORD_VOLUME, CHORD_CHANNEL)
#prog_minor = format_chords(prog_minor, CHORD_VOLUME, CHORD_CHANNEL)
#prog_all = format_chords(prog_all, CHORD_VOLUME, CHORD_CHANNEL)
#prog_play = prog_mayor

notes_play = keys.get_notes(key_play)

# Initialize Bar structures to store chords and melody notes
improv = Bar(key_play, (4, 4))
chords = Bar(key_play, (4, 4))

# Defines lists with different types of subdivisions
validSubdivisions = [2, 4, 4 / 3, 8, 8 / 3, 16, 16 / 3, 32, 32 / 3]
binarySubdivisions = [2, 4, 8, 16, 32]
simpleSubdivisions = [4, 8, 16]
simpleRests = [4, 8]
just16 = [16]

# Defines a list of the indexes of instruments that sound good playing chords
chord_instruments = [*range(1, 28)] + [*range(29, 45)] + [*range(46, 108)] + [*range(109, 113)] + [114] + [119] + [
    *range(122, 127)]

# Background Percussion
perc = Bar('C', (4, 4))
shaker = Note("A#", 5, None, PERC_VOLUME, PERC_CHANNEL)
perc.place_notes(Note("B", 1, None, PERC_VOLUME, PERC_CHANNEL), 8)
perc.place_notes(shaker, 4)
perc.place_notes(shaker, 8)
perc.place_notes(Note("B", 1, None, PERC_VOLUME, PERC_CHANNEL), 8)
perc.place_notes(shaker, 4)
perc.place_notes(shaker, 8)

while True:
    # Set Instruments
    chord_choice = choice(chord_instruments)
    melody_choice = randint(0, 127)
    fluidsynth.set_instrument(CHORD_CHANNEL, chord_choice)
    fluidsynth.set_instrument(MELODY_CHANNEL, melody_choice)

    # Random Chord Progression
    while not (chords.is_full()):
        chords.place_notes(NoteContainer(choice(prog_play)), 2)

    # Randomly Improvised Melody
    while not (improv.is_full()):  # Improvises melody
        if random() < 0.90:  # 90% chance of playing note
            improv.place_notes(Note(notes_play[randint(0, 6)], 5, None, MELODY_VOLUME, MELODY_CHANNEL),
                               choice(simpleSubdivisions))
        else:  # 10% Chance of silence
            improv.place_notes(None, choice(simpleRests))

    if random() < 0.3:  # 30% chance of duplicated melody
        midVal = len(improv.bar) // 2
        for i in range(midVal):
            improv[i + midVal] = improv[i][2]

    # Print Current Chords, Melody Notes and Instruments
    print_chords = []
    for i in chords:
        print_chords.append(i[2])
        if len(i[2].determine()) > 0:
            print_chords.append((i[2].determine())[0])
    print("Current Key: %s " % key_play)
    print("Current Chords: %s " % print_chords)
    print("Current Melody: %s " % improv)
    print("Chord Instrument: %i - %s " % (chord_choice, instrument.MidiInstrument.names[chord_choice]))
    print("Melody Instrument: %i - %s " % (melody_choice, instrument.MidiInstrument.names[melody_choice]))
    print()

    # Play Everything
    custom_play_bars([perc, improv, chords], 50)

    # Chance of repeating melody next bar
    if random() < 0.9:
        improv.empty()  # Resets melody 90% of the time

    # Chance of changing keys
    if random() < 0.15:  # 15% Chance
        dice = choice([*range(4)])
        if dice == 0:
            key_play = relative_modulation(key_play)
            print("KEY MODULATION! - Relative Key.")
        elif dice == 1:
            key_play = parallel_modulation(key_play)
            print("KEY MODULATION! - Parallel Key.")
        elif dice == 2:
            key_play = step_modulation(key_play, True)
            print("KEY MODULATION! - Step Up.")
        else:
            key_play = step_modulation(key_play, False)
            print("KEY MODULATION! - Step Down.")

        notes_play = keys.get_notes(key_play)
        prog_play = progressions.to_chords([minor_chords, mayor_chords][is_mayor(key_play)], key_play)
        prog_play = format_chords(prog_play, CHORD_VOLUME, CHORD_CHANNEL)
        if improv.is_full():
            improv.empty()

    chords.empty()

