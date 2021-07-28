import time

from mingus.core import scales, meter, chords, progressions
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
from random import randint, random, choice
from mingus.containers.instrument import Instrument, Piano, Guitar

fluidsynth.init("GeneralUserGSv1.471.sf2", "alsa")
# fluidsynth.init("TimGM6mb.sf2", "alsa")

prog = progressions.to_chords(["I", "V", "vi", "IV"], 'C')  # Sharp 2nd??
notes = scales.Ionian('C').ascending()
print(prog)

b = Bar('C', (4, 4))
for i in range(4):
    b + prog[i]

improv = Bar('C', (4, 4))

# currentChord = NoteContainer(['C-3', 'E-3', 'G-3'])
validSubdivisions = [2, 4, 4 / 3, 8, 8 / 3, 16, 16 / 3, 32, 32 / 3]
binarySubdivisions = [2, 4, 8, 16, 32]
simpleSubdivisions = [8, 16, 32]
just16 = [16]

while True:
    currentChord = NoteContainer(choice(prog))  # Random chord from progression
    # Lower 1 octave
    for i in range(len(currentChord)):
        aux = Note(currentChord[i])
        aux.octave_down()
        currentChord[i] = aux

    # for i in range(8):

    while not (improv.is_full()):  # Improvises melody
        if random() < 0.80:
            improv.place_notes(Note(notes[randint(0, 7)], 5), choice(just16))
        else:
            improv.place_notes(None, choice(just16))
    if random() < 0.3:  # 30% chance of duplicated melody
        midVal = len(improv.bar) // 2
        for i in range(midVal):
            improv[i + midVal] = improv[i][2]

    print(len(improv.bar))

    print(improv)
    fluidsynth.set_instrument(1, randint(0, 127))
    fluidsynth.play_NoteContainer(currentChord, 1, 20)

    # fluidsynth.main_volume(1, 20)
    fluidsynth.set_instrument(1, randint(0, 127))

    fluidsynth.play_Bar(improv, 1, 60)
    fluidsynth.stop_NoteContainer(currentChord, 1)
    if random() < 0.9:
        improv.empty()  # Resets melody 90% of the time
