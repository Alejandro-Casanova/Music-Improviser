import sys
import time

from mingus.core import scales, notes, keys
from mingus.containers import Note, Bar
from mingus.midi import fluidsynth
from random import randint, random, choice


def is_mayor(key):
    if key[0].isupper():
        return 1
    else:
        return 0


# Relative Modulation, changes the key to its corresponding mayor or minor relative
def relative_modulation(key):
    if type(key) is not str:
        print("Error: variable -key- must be a string.")
        sys.exit()
    if not keys.is_valid_key(key):
        print("Error in function -relative_modulation-. Invalid Key.")
        sys.exit()

    if key[0].isupper():
        return keys.relative_minor(key)
    else:
        return keys.relative_major(key)


# Parallel modulation, just changes mayor to minor or minor to mayor
def parallel_modulation(key):
    if type(key) is not str:
        print("Error: variable -key- must be a string.")
        sys.exit()
    if not keys.is_valid_key(key):
        print("Error in function -relative_modulation-. Invalid Key.")
        sys.exit()

    if is_mayor(key):
        if keys.get_key_signature(key) >= -4:
            key = keys.get_key(keys.get_key_signature(key) - 3)[1]
        else:
            key = keys.get_key(keys.get_key_signature(key) + 9)[1]
    else:
        if keys.get_key_signature(key) <= 4:
            key = keys.get_key(keys.get_key_signature(key) + 3)[0]
        else:
            key = keys.get_key(keys.get_key_signature(key) - 9)[0]
    return key


# Step modulation, moves one step up or down
def step_modulation(key, step_up=True):
    if type(key) is not str:
        print("Error: variable -key- must be a string.")
        sys.exit()
    if type(step_up) is not bool:
        print("Error: variable -step_up- must be a boolean.")
        sys.exit()
    if not keys.is_valid_key(key):
        print("Error in function -relative_modulation-. Invalid Key.")
        sys.exit()

    if step_up:
        if keys.get_key_signature(key) <= 0:
            key = keys.get_key(keys.get_key_signature(key) + 7)[1 - is_mayor(key)]
        else:
            key = keys.get_key(keys.get_key_signature(key) - 5)[1 - is_mayor(key)]
    else:
        if keys.get_key_signature(key) >= 0:
            key = keys.get_key(keys.get_key_signature(key) - 7)[1 - is_mayor(key)]
        else:
            key = keys.get_key(keys.get_key_signature(key) + 5)[1 - is_mayor(key)]
    return key


# Formats chord progression
def format_chords(prog_list, chord_volume=100, chord_channel=1):
    if type(prog_list) is not list:
        print("Error: variable -bars- must be a list of bars.")
        sys.exit()

    prog_aux = []
    for i in prog_list:
        aux = []
        for j in range(len(i)):
            if (j > 0) and (notes.note_to_int(i[j]) < notes.note_to_int(i[0])):
                aux.append(Note(i[j], 4, None, chord_volume, chord_channel))
            else:
                aux.append(Note(i[j], 3, None, chord_volume, chord_channel))
        prog_aux = prog_aux + [aux]
    return prog_aux


def custom_play_bars(bars, bpm):
    if type(bars) is not list:
        print("Error: variable -bars- must be a list of bars.")
        sys.exit()
    if type(bpm) is not int:
        print("Error: variable -bpm- must be an int.")
        sys.exit()

    # last_ticks = 0
    # ticks = time.clock()
    track = []
    for i in bars:
        for j in i:
            track.append([j[0], True, j[2]])
            track.append([j[0] + 1 / j[1], False, j[2]])

    def myFunc(e):
        return e[0]

    track.sort(key=myFunc)

    prev_ticks = time.perf_counter_ns()
    ticks = time.perf_counter_ns()
    dif_ticks = ticks - prev_ticks
    for i in track:
        if i[2] is None:
            continue
        play_ns = i[0] * 4 * 60 * 1000000000 / bpm  # Calculate moment to play note
        while dif_ticks < play_ns:
            ticks = time.perf_counter_ns()
            dif_ticks = ticks - prev_ticks
            pass
        if i[1]:
            fluidsynth.play_NoteContainer(i[2])
        else:
            fluidsynth.stop_NoteContainer(i[2])


def octave_down(chord_list):  # Receives 2D list ith chords and lowers them one octave down
    for i in range(len(chord_list)):
        for j in range(len(chord_list[i])):
            aux = Note(chord_list[i][j])
            aux.octave_down()
            chord_list[i][j] = aux


if __name__ == "__main__":
    fluidsynth.init("GeneralUserGSv1.471.sf2", "alsa")

    fluidsynth.set_instrument(1, 1)
    improv = Bar('C', (4, 4))
    perc = Bar('C', (4, 4))

    shaker = Note("A#", 5, None, 100, 9)
    perc.place_notes(Note("B", 1, None, 127, 9), 8)
    perc.place_notes(shaker, 4)
    perc.place_notes(shaker, 8)
    perc.place_notes(Note("B", 1, None, 127, 9), 8)
    perc.place_notes(shaker, 4)
    perc.place_notes(shaker, 8)

    notes = scales.Ionian('C').ascending()

    while not (improv.is_full()):  # Improvises melody
        if random() < 0.90:  # 80% chance of playing note
            improv.place_notes(Note(notes[randint(0, 7)], 5, None, 100, 2), choice([4, 8, 16]))
        else:  # 20% Chance of silence
            improv.place_notes(None, 16)

    while True:
        fluidsynth.play_Bar(perc, bpm=50)
        fluidsynth.play_Bar(improv, bpm=50)
        custom_play_bars([improv, perc], 50)
