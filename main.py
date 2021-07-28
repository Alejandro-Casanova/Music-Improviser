import time

from mingus.core import scales, meter, chords, progressions
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
from random import randint, random, choice
from mingus.containers.instrument import Instrument, Piano, Guitar

CHORD_VOLUME = 65
MELODY_VOLUME = 100

def octave_down(chord_list):  # Receives 2D list ith chords and lowers them one octave down
    for i in range(len(chord_list)):
        for j in range(len(chord_list[i])):
            aux = Note(chord_list[i][j])
            aux.octave_down()
            chord_list[i][j] = aux


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
#octave_down(prog2)

improv = Bar('C', (4, 4))

# Defines lists with different types of subdivisions
validSubdivisions = [2, 4, 4 / 3, 8, 8 / 3, 16, 16 / 3, 32, 32 / 3]
binarySubdivisions = [2, 4, 8, 16, 32]
simpleSubdivisions = [8, 16, 32]
just16 = [16]

# Defines a list of the indexes of instruments that sound good playing chords
chord_instruments = [*range(1, 28)] + [*range(29, 45)] + [*range(46, 108)] + [*range(109, 113)] + [114] + [119] + [
    *range(122, 127)]

while True:
    fluidsynth.set_instrument(1, choice(chord_instruments))
    fluidsynth.set_instrument(2, randint(0, 127))
    currentChord = NoteContainer(choice(prog2))  # Random chord from progression

    while not (improv.is_full()):  # Improvises melody
        if random() < 0.80:  # 80% chance of playing note
            improv.place_notes(Note(notes[randint(0, 7)], 5, None, MELODY_VOLUME, 2), choice(just16))
        else:  # 20% Chance of silence
            improv.place_notes(None, choice(just16))

        # Background Percussion
        if improv.is_full():
            shaker = Note("A#", 5, None, 100, 9)
            #improv = Bar()
            improv.place_notes_at(Note("B", 1, None, 127, 9), 0.0)
            improv.place_notes_at(shaker, 0.125)
            improv.place_notes_at(shaker, 0.375)
            improv.place_notes_at(Note("B", 1, None, 127, 9), 0.5)
            improv.place_notes_at(shaker, 0.625)
            improv.place_notes_at(shaker, 0.875)

    if random() < 0.3:  # 30% chance of duplicated melody
        midVal = len(improv.bar) // 2
        for i in range(midVal):
            improv[i + midVal] = improv[i][2]

    # print(len(improv.bar))
    print(currentChord)
    print(improv)
    fluidsynth.play_NoteContainer(currentChord, 1)

    fluidsynth.play_Bar(improv, 1, 60)
    #fluidsynth.play_Bars([drums2, improv], [1, 9], 60)
    fluidsynth.stop_NoteContainer(currentChord, 1)
    if random() < 0.9:
        improv.empty()  # Resets melody 90% of the time
