import random

class ScaleGenerator:
    """Class to generate chords for major, minor, and harmonic minor scales in any key."""

    # 🎹 Note mappings (C to B)
    NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # 🎵 Scale degree patterns for Major, Minor, and Harmonic Minor
    SCALE_PATTERNS = {
        "major": [0, 2, 4, 5, 7, 9, 11],   # I ii iii IV V vi vii°
        "minor": [0, 2, 3, 5, 7, 8, 10],   # i ii° III iv v VI VII
        "hminor": [0, 2, 3, 5, 7, 8, 11]   # i ii° III iv V VI vii°
    }

    # 🎵 Chord qualities for each scale type
    CHORD_QUALITIES = {
        "major": ["M", "m", "m", "M", "M", "m", "dim"],
        "minor": ["m", "dim", "M", "m", "m", "M", "M"],
        "hminor": ["m", "dim", "M", "m", "M", "M", "dim"]  # V is major, vii° is diminished
    }

    def __init__(self):
        """Initialize the class and precompute all possible scales."""
        self.ALL_SCALES = self.generate_all_scales()

    def get_scale_notes(self, root_note, scale_type):
        """Generate the scale notes for the given root and scale type."""
        if root_note not in self.NOTE_NAMES or scale_type not in self.SCALE_PATTERNS:
            raise ValueError("Invalid root note or scale type.")
        
        root_index = self.NOTE_NAMES.index(root_note)
        scale_intervals = self.SCALE_PATTERNS[scale_type]
        return [self.NOTE_NAMES[(root_index + interval) % 12] for interval in scale_intervals]

    def generate_chords(self, root_note, scale_type):
        """Generate chords for a given key and scale type."""
        scale_notes = self.get_scale_notes(root_note, scale_type)
        chord_names = ["I", "ii", "iii", "IV", "V", "vi", "vii°"] if scale_type == "major" else \
                      ["i", "ii°", "III", "iv", "v", "VI", "VII"]
        
        # Use the correct chord qualities
        chord_qualities = self.CHORD_QUALITIES[scale_type]
        chords = {}
        for degree, (note, quality) in enumerate(zip(scale_notes, chord_qualities)):
            chord_symbol = chord_names[degree]  # Get Roman numeral
            chords[chord_symbol] = f"{note}{quality}"  # Example: C Major → CM, D Minor → Dm
        return chords

    def generate_all_scales(self):
        """Precompute chords for all keys and scale types."""
        all_scales = {}
        for note in self.NOTE_NAMES:
            all_scales[note] = {
                "major": self.generate_chords(note, "major"),
                "minor": self.generate_chords(note, "minor"),
                "hminor": self.generate_chords(note, "hminor")
            }
        return all_scales

    def display_chords(self, root_note, scale_type):
        """Display the chords for a specific key and scale type."""
        if root_note in self.ALL_SCALES and scale_type in self.SCALE_PATTERNS:
            print(f"\n🎵 Chords in {root_note} {scale_type.capitalize()} Scale:")
            for roman, chord in self.ALL_SCALES[root_note][scale_type].items():
                print(f"{roman}: {chord}")
        else:
            print("⚠️ Invalid input! Enter a valid note (C, D#, Bb, etc.) and scale type (major/minor/hminor).")

    def display_all_scales(self):
        """Display all scales for all keys."""
        for root, scales in self.ALL_SCALES.items():
            print(f"\n🎵 {root} Major Scale Chords: {scales['major']}")
            print(f"🎵 {root} Minor Scale Chords: {scales['minor']}")
            print(f"🎵 {root} Harmonic Minor Scale Chords: {scales['hminor']}")

