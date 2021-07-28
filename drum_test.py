import time

from mingus.core import scales, meter, chords, progressions
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
from random import randint, random, choice, randrange
from mingus.containers.instrument import Instrument, Piano, Guitar

fluidsynth.init("GeneralUserGSv1.471.sf2", "alsa")
fluidsynth.set_instrument(1, 127)
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Bass Drum: B-1, C-2
# High Hat F#-2, G#-2, A#-2 (open)
drums = Bar()
drums.place_notes(Note("B", 1, None, 100, 9), 8)
drums.place_notes(Note("F#", 2, None, 100, 9), 4)
drums.place_notes(Note("F#", 2, None, 100, 9), 8)
drums.place_notes(Note("B", 1, None, 100, 9), 8)
drums.place_notes(Note("F#", 2, None, 100, 9), 4)
drums.place_notes(Note("F#", 2, None, 100, 9), 8)

shaker = Note("A#", 5, None, 100, 9)
drums2 = Bar()
drums2.place_notes(Note("B", 1, None, 127, 9), 8)
drums2.place_notes(shaker, 4)
drums2.place_notes(shaker, 8)
drums2.place_notes(Note("B", 1, None, 127, 9), 8)
drums2.place_notes(shaker, 4)
drums2.place_notes(shaker, 8)

while True:
    fluidsynth.play_Bar(drums2, 1, 60)
while True:
    for i in range(1, 7):
        for j in range(12):
            print(notes[j], "-", i)
            fluidsynth.play_Note(Note(notes[j], i, None, 127, 9))
            time.sleep(1)
            fluidsynth.stop_Note(Note(notes[j], i, None, 127, 9))
