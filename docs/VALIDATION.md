# Validation and test results

## On-device result

The generated firmware was successfully installed and tested on one Creative Stage SE MF8410. The soundbar booted normally, and the embedded prompts played at the reduced volume.

This is evidence of compatibility with that unit, not a guarantee for every hardware revision.

## Output

- All embedded MP3 prompts reduced using in-place MP3 global gain
- Requested amplitude: 15%
- Actual amplitude: **14.8651%**
- MP3 re-encoding: none
- Firmware size: 815,616 bytes before and after
- Official OTA SHA-256: `08a56e7e08e36e1623feb29427eb9f36a403b76829abd6edfe004e93841976ab`
- Patched OTA SHA-256: `e298034b4df9669b03781e21128b631ee30c5328a1388b41cab7bb2b2667358c`
- Patch SHA-256: `4591522de899859f93acbce32d2be7ea6a8db8db0a5c928a6a6ffbcdb30eb9e4`
- Replacement bytes in OTA: 7,332
- Patch hunks: 625

## Structural validation

- Vendor transform decrypt/re-encrypt round trip: PASS
- SDFS directory checksum: PASS
- SDFS data checksum: PASS
- All 17 SDFS entry tags: PASS
- AOTA header CRC-32: PASS
- AOTA aggregate data CRC-32: PASS
- All 5 AOTA entry CRC-32 values: PASS
- Manifest checksum synchronised with encrypted `sdfs.bin`: PASS
- All 12 MP3 files decoded after modification: PASS
- Decoded waveform correlation: 1.000000000 for every MP3

## Modified prompt assets

| Internal name | Bytes | Frames | Duration | Decoded amplitude | Correlation |
|---|---:|---:|---:|---:|---:|
| `btcntd.mp3` | 3,168 | 44 | 1.584 s | 14.8651% | 1.000000000 |
| `btdisc.mp3` | 3,456 | 48 | 1.728 s | 14.8651% | 1.000000000 |
| `btwpr.mp3` | 6,048 | 84 | 3.024 s | 14.8651% | 1.000000000 |
| `callring.mp3` | 2,520 | 35 | 1.260 s | 14.8651% | 1.000000000 |
| `dot.mp3` | 1,944 | 27 | 0.972 s | 14.8651% | 1.000000000 |
| `eof.mp3` | 3,816 | 53 | 1.908 s | 14.8651% | 1.000000000 |
| `eon.mp3` | 3,456 | 48 | 1.728 s | 14.8651% | 1.000000000 |
| `mode1.mp3` | 864 | 12 | 0.432 s | 14.8651% | 1.000000000 |
| `reset.mp3` | 4,104 | 57 | 2.052 s | 14.8651% | 1.000000000 |
| `tts_off.mp3` | 3,744 | 52 | 1.872 s | 14.8651% | 1.000000000 |
| `tts_on.mp3` | 3,456 | 48 | 1.728 s | 14.8651% | 1.000000000 |
| `version.mp3` | 7,056 | 98 | 3.528 s | 14.8651% | 1.000000000 |
