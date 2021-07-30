import time

from mingus.core import scales, meter, chords, progressions
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
from random import randint, random, choice
from play_bars_test import custom_play_bars  # My custom function

CHORD_VOLUME = 65
MELODY_VOLUME = 100

fluidsynth.init("GeneralUserGSv1.471.sf2", "alsa")
# fluidsynth.init("TimGM6mb.sf2", "alsa")

prog = progressions.to_chords(["I", "V", "vi", "IV"], 'C')  # Sharp 2nd??
notes = scales.Ionian('C').ascending()

# Formats chord progression
prog2 = []
for i in prog:
    #prog2 = prog2 + [NoteContainer(i).notes]
    aux = []
    for j in range(len(i)):
        aux.append(Note(i[j], 3, None, CHORD_VOLUME, 1))
    prog2 = prog2 + [aux]
print(prog2)

improv = Bar('C', (4, 4))

# Defines lists with different types of subdivisions
validSubdivisions = [2, 4, 4 / 3, 8, 8 / 3, 16, 16 / 3, 32, 32 / 3]
binarySubdivisions = [2, 4, 8, 16, 32]
simpleSubdivisions = [4, 8, 16]
simpleRests = [4, 8]
just16 = [16]

# Defines a list of the indexes of instruments that sound good playing chords
chord_instruments = [*range(1, 28)] + [*range(29, 45)] + [*range(46, 108)] + [*range(109, 113)] + [114] + [119] + [
    *range(122, 127)]

while True:
    fluidsynth.set_instrument(1, choice(chord_instruments))
    fluidsynth.set_instrument(2, randint(0, 127))
    currentChord = NoteContainer(choice(prog2))  # Random chord from progression

    # Improvised Melody
    while not (improv.is_full()):  # Improvises melody
        if random() < 0.80:  # 80% chance of playing note
            improv.place_notes(Note(notes[randint(0, 7)], 5, None, MELODY_VOLUME, 2), choice(just16))
        else:  # 20% Chance of silence
            improv.place_notes(None, choice(just16))

    # Background Percussion
    perc = Bar('C', (4, 4))
    shaker = Note("A#", 5, None, 100, 9)
    perc.place_notes(Note("B", 1, None, 127, 9), 8)
    perc.place_notes(shaker, 4)
    perc.place_notes(shaker, 8)
    perc.place_notes(Note("B", 1, None, 127, 9), 8)
    perc.place_notes(shaker, 4)
    perc.place_notes(shaker, 8)

    if random() < 0.3:  # 30% chance of duplicated melody
        midVal = len(improv.bar) // 2
        for i in range(midVal):
            improv[i + midVal] = improv[i][2]

    print(currentChord)
    print(improv)
    fluidsynth.play_NoteContainer(currentChord, 1)

    custom_play_bars([perc, improv], 50)

    fluidsynth.stop_NoteContainer(currentChord, 1)
    if random() < 0.9:
        improv.empty()  # Resets melody 90% of the time
