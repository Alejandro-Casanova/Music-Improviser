import time

from mingus.core import scales, meter, chords, progressions
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
from random import randint, random, choice
from mingus.containers.instrument import Instrument, Piano, Guitar

fluidsynth.init("GeneralUserGSv1.471.sf2", "alsa")

while True:
    currentChord = NoteContainer(["C", "E", "G"])  # Random chord from progression
    # Lower 1 octave
    for i in range(len(currentChord)):
        aux = Note(currentChord[i])
        aux.octave_down()
        currentChord[i] = aux


    for i in range(105, 200):
        print(i)
        fluidsynth.set_instrument(1, i)
        fluidsynth.play_NoteContainer(currentChord, 1, 20)
        time.sleep(2.0)
        fluidsynth.stop_NoteContainer(currentChord, 1)
