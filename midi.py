import mido
from mido import Message, MidiFile, MidiTrack
import random
import pygame

# 🎵 MIDI note mappings
CHORDS = {
    "I": [60, 64, 67],     # C major (C, E, G)
    "ii": [62, 65, 69],    # D minor (D, F, A)
    "iii": [64, 67, 71],   # E minor (E, G, B)
    "IV": [65, 69, 72],    # F major (F, A, C)
    "V": [67, 71, 74],     # G major (G, B, D)
    "vi": [69, 72, 76],    # A minor (A, C, E)
    "vii": [71, 74, 77]     # B diminished (B, D, F)
}

# 🎶 Note durations at 120 BPM
NOTE_DURATIONS = {
    "chord": 960,    # Hold chords longer (was too short before)
    "overlap": 20,   # Slight overlap to avoid total silence
    "rest": 3       # Minimize rest to reduce large gaps
}

def create_midi(chord_progression, filename="output.mid", bpm=120):
    """Generate MIDI with smoother chord transitions and reduced silence."""
    
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo
    tempo = mido.bpm2tempo(bpm)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    for chord in chord_progression:
        if chord not in CHORDS:
            continue  # Skip invalid chords
        
        notes = CHORDS[chord]

        # 🎸 Play chord notes
        for note in notes:
            track.append(Message('note_on', note=note, velocity=80, time=0))

        # ⏳ Hold chord (add overlap to reduce silence)
        track.append(Message('note_off', note=notes[0], velocity=80, time=NOTE_DURATIONS["chord"] - NOTE_DURATIONS["overlap"]))

        # 🎼 Release notes (ensuring minimal silence)
        for note in notes[1:]:
            track.append(Message('note_off', note=note, velocity=80, time=NOTE_DURATIONS["rest"]))
    mid.save(filename)
    print(f"MIDI saved: {filename}")

def play_midi(midi_file):
    pygame.init()
    pygame.mixer.init()
    print("🎮 Playing MIDI file in 8-bit mode...")
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(2)