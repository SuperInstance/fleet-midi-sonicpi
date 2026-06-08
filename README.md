<div align="center">

# 💫 fleet-midi-sonicpi

> *Timing-critical MIDI clock patterns for fleet agents*

[![CI](https://img.shields.io/github/actions/workflow/status/SuperInstance/fleet-midi-sonicpi/ci.yml?style=flat-square&logo=github&label=CI)](https://github.com/SuperInstance/fleet-midi-sonicpi/actions)
[![npm](https://img.shields.io/badge/npm-%40superinstance%2Fmidi--sonicpi-cb3837?style=flat-square&logo=npm)](https://www.npmjs.com/package/@superinstance/midi-sonicpi)
[![Docker](https://img.shields.io/badge/docker-ghcr-2496ed?style=flat-square&logo=docker)](https://github.com/SuperInstance/fleet-midi-sonicpi/pkgs/container/fleet-midi-sonicpi)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](http://makeapullrequest.com)

---

Generates Sonic Pi live_loop patterns from agent note data. Strict timing guarantees keep complex generative loops in sync. HTTP endpoint turns fleet decisions into playable Sonic Pi code.

---

## 📦 Installation

```bash
# npm
npm install @superinstance/midi-sonicpi

# Docker
docker pull ghcr.io/superinstance/fleet-midi-sonicpi:latest

# Clone
git clone https://github.com/SuperInstance/fleet-midi-sonicpi.git
```

## 🚀 Quick Start

```bash
# POST notes, get Sonic Pi code:
curl -X POST localhost:3006 \
  -H "Content-Type: application/json" \
  -d "{\"notes\":[60,64,67,72],\"bpm\":120}"

# Direct import:
from lib.server import sonici_pi_pattern
code = sonici_pi_pattern([60,64,67,60,67,64], 90)
print(code)
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Fleet Note Data           Sonic Pi Code            │
│   [60, 64, 67, 72]          live_loop :fleet_agent  │
│         │                    play :C4                │
│         ▼                    sleep 0.5               │
│   ┌──────────────┐          play :E4                │
│   │ Pattern      │───▶      sleep 0.5               │
│   │ Builder      │          play :G4                │
│   └──────────────┘          sleep 0.5               │
│         │                   end                      │
│         ▼                                            │
│   HTTP POST :3006/notes  →  Ready for Sonic Pi paste │
│                                                     │
│   Timing-exact: use_bpm keeps everything in sync     │
└─────────────────────────────────────────────────────┘
```

## 📡 API

### POST /notes
Send note list and BPM → receive executable Sonic Pi live_loop code.

```json
{"notes": [60, 64, 67, 72], "bpm": 120}
```
→ Returns `use_bpm 120` live_loop with `play :C4, sleep 0.5` pattern.

## 🧪 Beta Tested

Part of the [SuperInstance MIDI Fleet](https://github.com/SuperInstance/construct-coordination/blob/main/FLEET_MIDI.md). Every push verified via CI — zeroshot tests ensure zero-config operation out of the box.

## 🤝 Related

- [fleet-bridge](https://github.com/SuperInstance/fleet-bridge) — I2I bottle transport
- [construct-coordination](https://github.com/SuperInstance/construct-coordination) — Fleet catalog

---

<div align="center">
<sub>Built with 💫 for the SuperInstance fleet • <a href="https://github.com/SuperInstance">github.com/SuperInstance</a></sub>
</div>
