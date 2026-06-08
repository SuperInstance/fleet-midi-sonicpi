"""Sonic Pi bridge — real-time MIDI playback for the fleet.

Generates Sonic Pi live_loop code from MIDI note data.
Paste the output into Sonic Pi for sub-millisecond timing accuracy.
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

NOTE_NAMES = ['C','Cs','D','Ds','E','F','Fs','G','Gs','A','As','B']

def note_name(midi: int) -> str:
    """Convert MIDI number to Sonic Pi notation (e.g. 60 → :C4)."""
    octave = (midi // 12) - 1
    name = NOTE_NAMES[midi % 12]
    return f":{name}{octave}"

def generate_live_loop(notes: list, bpm: int = 120, loop_name: str = "fleet_agent") -> str:
    """Generate a complete Sonic Pi live_loop from note data."""
    sleep_val = 60.0 / bpm / 4  # sixteenth notes at given BPM
    code = f"use_bpm {bpm}\n\nlive_loop :{loop_name} do\n"
    for n in notes:
        pitch = n['pitch'] if isinstance(n, dict) else n
        vel = n.get('velocity', 100) if isinstance(n, dict) else 100
        dur = n.get('duration', 1) if isinstance(n, dict) else 1
        code += f"  synth :pretty_bell, note: {note_name(pitch)}, amp: {vel/127:.2f}, release: {dur * sleep_val:.3f}\n"
        code += f"  sleep {dur * sleep_val:.3f}\n"
    code += "end"
    return code

def generate_from_pattern(ternary_vector: list, bpm: int = 120) -> str:
    """Generate Sonic Pi pattern from a ternary vector.
    
    +1 → high bell (assertion)
    0  → medium pulse (sustain)
    -1 → low thud (opposition)
    """
    base_pitch = 60
    notes = []
    for v in ternary_vector:
        if v == 1:
            notes.append({'pitch': base_pitch + 4, 'velocity': 120, 'duration': 1})
            base_pitch += 1
        elif v == -1:
            notes.append({'pitch': base_pitch - 4, 'velocity': 80, 'duration': 1})
            base_pitch -= 1
        else:
            notes.append({'pitch': base_pitch, 'velocity': 60, 'duration': 1})
    
    pattern_name = "fleet_" + ''.join(str(max(0, v)) for v in ternary_vector[:4])
    return generate_live_loop(notes, bpm, pattern_name)

class SonicPiHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = json.loads(self.rfile.read(content_length))
        else:
            body = {}
        
        notes = body.get('notes', [60, 64, 67])
        bpm = body.get('bpm', 120)
        
        if 'ternary_vector' in body:
            code = generate_from_pattern(body['ternary_vector'], bpm)
        else:
            code = generate_live_loop(notes, bpm)
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(code.encode())
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "service": "sonicpi", "ensign": "Pulse"}).encode())

if __name__ == '__main__':
    print("💫 Pulse — Fleet Sonic Pi Officer")
    print("   Serving on :3006")
    print("   POST / with {notes: [60,64,67], bpm: 120}")
    print("   POST / with {ternary_vector: [1,0,-1,1]}")
    HTTPServer(('', 3006), SonicPiHandler).serve_forever()
