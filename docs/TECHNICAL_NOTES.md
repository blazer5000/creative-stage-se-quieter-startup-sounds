# Technical notes

## Modification

The official v1001 firmware contains 12 MP3 prompt assets. Their MP3 `global_gain` values were reduced uniformly using an in-place lossless transformation.

- Requested linear amplitude: 15%
- Representable amplitude selected: **14.8651%**
- Approximate change: **−16.56 dB**
- MP3 re-encoding: none
- MP3 file-size changes: none
- Firmware-size change: none

MP3 gain is quantised, so precisely 15% cannot be represented without re-encoding. The selected setting is the nearest valid in-place gain step.

## Patch design

`patches/stage-se-v1001-quieter-prompts.stsep` is an exact-input binary patch. It contains replacement bytes only—not Creative's complete firmware or extracted audio.

The patcher:

1. Accepts Creative's official ZIP or extracted `ota.bin`.
2. Requires exact size 815,616 bytes.
3. Requires official SHA-256 `08a56e7e08e36e1623feb29427eb9f36a403b76829abd6edfe004e93841976ab`.
4. Applies sorted, non-overlapping replacement hunks.
5. Requires output SHA-256 `e298034b4df9669b03781e21128b631ee30c5328a1388b41cab7bb2b2667358c`.
6. Writes the result atomically only after validation.

This narrow patch approach intentionally does not publish a general-purpose firmware decryption tool, vendor key or extracted prompt bank.

## Integrity checks performed

- Vendor transform decrypt/re-encrypt round trip
- SDFS directory and aggregate data checksums
- All SDFS entry tags
- AOTA header and aggregate data CRC-32
- All AOTA entry CRC-32 values
- Manifest checksum synchronisation
- Decoding of all 12 modified MP3 streams
- Decoded waveform correlation of 1.000000000 for each prompt

See [VALIDATION.md](VALIDATION.md) for hashes and per-file results.
