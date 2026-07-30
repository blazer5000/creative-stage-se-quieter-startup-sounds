# Detailed installation guide

## Before starting

- Confirm the label says **Creative Stage SE**, model **MF8410**.
- Do not use this patch on Creative Stage SE mini or any other Stage model.
- Obtain `Creative Stage SE FW Update v1001.zip` directly from Creative.
- Use a reliable power outlet. Do not perform the update where power may be interrupted.
- Keep the official firmware package.

## Generate the firmware

The patcher accepts either Creative's complete ZIP or the extracted `ota.bin`. It validates the exact official SHA-256 before changing anything. Unsupported inputs are rejected without writing output.

Windows drag-and-drop:

1. Extract this repository ZIP.
2. Drag Creative's official firmware ZIP onto `make_quieter_firmware_windows.bat`.
3. Find the generated `Creative_Stage_SE_quieter_prompts/ota.bin` beside the official ZIP.

Command line:

```text
python make_quieter_firmware.py <official ZIP or ota.bin>
```

Optional arguments:

```text
-o, --output <path>   Choose the output filename
--force               Replace an existing output
--self-test           Validate the included patch without firmware
```

## Flashing

1. Prepare an empty thumb drive below 32 GB using FAT16/FAT32 and MBR.
2. Put only the generated `ota.bin` in the root directory.
3. Turn the soundbar off.
4. Insert the drive into the rear USB-A firmware port.
5. Connect the adapter and power on.
6. Wait while the LED blinks red.
7. Do not touch power, the drive or the soundbar until blinking stops.
8. Power off, unplug the adapter and remove the drive.
9. Reconnect power and start the soundbar.

## After installation

Test power on/off, USB mode, Bluetooth connection/disconnection, voice-prompt toggle and reset prompts. Normal playback volume should be unaffected.

If the LED continues blinking indefinitely or the unit does not restart, do not repeatedly interrupt and restart flashing. Seek assistance and describe exactly what occurred.
