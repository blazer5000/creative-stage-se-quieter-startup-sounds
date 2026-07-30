# Creative Stage SE quieter startup sounds

**Fix the loud startup / power-on sound and voice prompts on the Creative Stage SE soundbar (model MF8410).**

This repository creates an unofficial firmware file that reduces all 12 built-in MP3 prompts—including power on, power off, Bluetooth and reset sounds—to **14.8651% of their original amplitude**. Normal music, movie and game playback volume is not changed.

> [!WARNING]
> This is unofficial firmware and is not endorsed by Creative Technology. It was successfully installed and tested on one Creative Stage SE MF8410, but firmware updates always carry risk. Use only with the exact supported model and firmware. Never interrupt power during flashing.

## Why this exists

The Creative Stage SE has loud built-in startup and status sounds with no documented prompt-volume control. This patch makes those sounds substantially quieter while leaving the soundbar's normal audio behaviour unchanged.

Search terms: Creative Stage SE loud startup sound, Creative Stage SE power-on volume, Stage SE startup chime too loud, MF8410 firmware patch, quieter voice prompts.

## Compatibility

| Item | Supported |
|---|---|
| Product | Creative Stage SE |
| Model | MF8410 |
| Official base package | `Creative Stage SE FW Update v1001.zip` |
| Official release | Firmware v1.0.0.1 / v1001 |
| Official `ota.bin` SHA-256 | `08a56e7e08e36e1623feb29427eb9f36a403b76829abd6edfe004e93841976ab` |
| Patched `ota.bin` SHA-256 | `e298034b4df9669b03781e21128b631ee30c5328a1388b41cab7bb2b2667358c` |
| Creative Stage SE mini | **No** |
| Other Creative Stage models | **No** |

Download the official firmware from [Creative's Stage SE support page](https://support.creative.com/Products/ProductDetails.aspx?catID=4&prodID=24120&subCatID=848). This repository does **not** contain or redistribute Creative's firmware or extracted prompt audio.

## Easiest method

### Windows: drag and drop

1. Download this repository using **Code → Download ZIP**, then extract it.
2. Download `Creative Stage SE FW Update v1001.zip` from Creative.
3. Drag Creative's ZIP onto `make_quieter_firmware_windows.bat`.
4. A new folder named `Creative_Stage_SE_quieter_prompts` will be created beside Creative's ZIP.
5. Confirm it contains `ota.bin`.

### Windows command line

```powershell
py -3 make_quieter_firmware.py "C:\Users\you\Downloads\Creative Stage SE FW Update v1001.zip"
```

### macOS or Linux

```bash
python3 make_quieter_firmware.py ~/Downloads/'Creative Stage SE FW Update v1001.zip'
```

The patcher refuses unsupported files and verifies both the official input and patched output using SHA-256.

## Install on the soundbar

1. Use an empty USB thumb drive below 32 GB, formatted FAT16 or FAT32 with an MBR partition table.
2. Copy the generated `ota.bin` to the root of the thumb drive.
3. Power off the Creative Stage SE.
4. Insert the thumb drive into the soundbar's USB-A firmware-update port.
5. Connect the power adapter and turn the soundbar on.
6. The LED should blink red while flashing.
7. **Do not disconnect power or remove the thumb drive.**
8. Wait until the red LED stops blinking.
9. Power off the soundbar and disconnect both the adapter and thumb drive.
10. Reconnect the adapter and turn the soundbar on.

These steps follow Creative's official update procedure; only the locally generated `ota.bin` differs.

## What is changed

- All 12 embedded MP3 prompt files are reduced to 14.8651% amplitude.
- The nearest lossless MP3 global-gain step was used; the requested 15% cannot be represented exactly.
- MP3 streams are not re-encoded.
- Prompt lengths, file sizes and waveforms remain unchanged apart from amplitude.
- Firmware executable code, boot image and system parameters are not intentionally modified.

See [technical notes](docs/TECHNICAL_NOTES.md) and [validation results](docs/VALIDATION.md).

## Can this brick the soundbar?

No firmware modification can be described as risk-free. The patched image passed all identified checksums and successfully ran on one unit, but no documented consumer recovery procedure has been confirmed. Keep Creative's official package and do not interrupt an update.

## Legal and copyright position

This repository distributes only original documentation, patching code and the minimal binary difference needed to transform a user-supplied official file. It does not distribute Creative's original or modified complete firmware, its extracted MP3 files, logos or artwork. See [DISCLAIMER.md](DISCLAIMER.md).

## Contributing

Reports from additional MF8410 units are useful. Please include the model printed on the device, official input SHA-256, operating system used for patching and whether installation completed. Do not upload Creative firmware or extracted audio to an issue.

## Licence

The patching code and repository documentation are licensed under the [MIT License](LICENSE). Creative's firmware remains the property of its respective owner and is not covered by this licence.
