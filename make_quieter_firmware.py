#!/usr/bin/env python3
"""Create quieter Creative Stage SE firmware from Creative's official v1001 package.

This program contains no Creative firmware. It applies a narrow binary patch only
when the official input's exact SHA-256 matches the supported release.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

SUPPORTED_MODEL = "Creative Stage SE (MF8410)"
EXPECTED_SIZE = 815_616
OFFICIAL_SHA256 = "08a56e7e08e36e1623feb29427eb9f36a403b76829abd6edfe004e93841976ab"
PATCHED_SHA256 = "e298034b4df9669b03781e21128b631ee30c5328a1388b41cab7bb2b2667358c"
PATCH_SHA256 = "4591522de899859f93acbce32d2be7ea6a8db8db0a5c928a6a6ffbcdb30eb9e4"
PATCH_FILE = Path(__file__).resolve().parent / "patches" / "stage-se-v1001-quieter-prompts.stsep"


class PatchError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_official_input(path: Path) -> bytes:
    if not path.is_file():
        raise PatchError(f"Input file does not exist: {path}")

    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            candidates = [
                name for name in archive.namelist()
                if Path(name).name.lower() == "ota.bin" and not name.endswith("/")
            ]
            if len(candidates) != 1:
                raise PatchError(
                    "Expected exactly one ota.bin inside the ZIP; "
                    f"found {len(candidates)}."
                )
            info = archive.getinfo(candidates[0])
            if info.file_size > 2_000_000:
                raise PatchError("Refusing unexpectedly large ota.bin.")
            return archive.read(candidates[0])

    return path.read_bytes()


def parse_patch(data: bytes) -> tuple[int, bytes, bytes, list[tuple[int, bytes]]]:
    minimum = 8 + 4 + 32 + 32 + 4
    if len(data) < minimum or data[:8] != b"STSEPAT1":
        raise PatchError("Invalid or unsupported patch file.")

    position = 8
    file_size = struct.unpack_from("<I", data, position)[0]
    position += 4
    input_hash = data[position:position + 32]
    position += 32
    output_hash = data[position:position + 32]
    position += 32
    hunk_count = struct.unpack_from("<I", data, position)[0]
    position += 4

    if hunk_count > 100_000:
        raise PatchError("Patch hunk count is implausible.")

    hunks: list[tuple[int, bytes]] = []
    previous_end = 0
    for _ in range(hunk_count):
        if position + 6 > len(data):
            raise PatchError("Patch file is truncated.")
        offset, length = struct.unpack_from("<IH", data, position)
        position += 6
        end = position + length
        if end > len(data):
            raise PatchError("Patch replacement data is truncated.")
        if offset < previous_end or offset + length > file_size:
            raise PatchError("Patch contains overlapping or out-of-range hunks.")
        hunks.append((offset, data[position:end]))
        previous_end = offset + length
        position = end

    if position != len(data):
        raise PatchError("Patch has unexpected trailing data.")
    return file_size, input_hash, output_hash, hunks


def load_and_validate_patch() -> tuple[int, bytes, bytes, list[tuple[int, bytes]]]:
    if not PATCH_FILE.is_file():
        raise PatchError(f"Patch file is missing: {PATCH_FILE}")
    patch_data = PATCH_FILE.read_bytes()
    actual_patch_hash = sha256(patch_data)
    if actual_patch_hash != PATCH_SHA256:
        raise PatchError(
            "Patch file checksum mismatch. Download a fresh copy of the repository.\n"
            f"Expected: {PATCH_SHA256}\nActual:   {actual_patch_hash}"
        )
    return parse_patch(patch_data)


def apply_patch(original: bytes, hunks: list[tuple[int, bytes]]) -> bytes:
    result = bytearray(original)
    for offset, replacement in hunks:
        result[offset:offset + len(replacement)] = replacement
    return bytes(result)


def default_output_path(input_path: Path) -> Path:
    return input_path.resolve().parent / "Creative_Stage_SE_quieter_prompts" / "ota.bin"


def write_atomically(path: Path, data: bytes, force: bool) -> None:
    path = path.resolve()
    if path.exists() and not force:
        raise PatchError(f"Output already exists: {path}\nUse --force to replace it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".ota-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


def self_test() -> int:
    file_size, input_hash, output_hash, hunks = load_and_validate_patch()
    if file_size != EXPECTED_SIZE:
        raise PatchError("Patch declares the wrong firmware size.")
    if input_hash.hex() != OFFICIAL_SHA256:
        raise PatchError("Patch declares the wrong official input hash.")
    if output_hash.hex() != PATCHED_SHA256:
        raise PatchError("Patch declares the wrong patched output hash.")
    changed = sum(len(replacement) for _, replacement in hunks)
    print("Self-test passed")
    print(f"Patch: {PATCH_FILE.name}")
    print(f"Hunks: {len(hunks)}")
    print(f"Replacement bytes: {changed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Create quieter firmware prompts for Creative Stage SE (MF8410) "
            "from Creative's official v1001 ZIP or ota.bin."
        )
    )
    parser.add_argument("input", nargs="?", type=Path, help="Official firmware ZIP or ota.bin")
    parser.add_argument("-o", "--output", type=Path, help="Output path; defaults beside the input")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    parser.add_argument("--self-test", action="store_true", help="Validate the included patch and exit")
    args = parser.parse_args()

    try:
        if args.self_test:
            return self_test()
        if args.input is None:
            parser.error("input is required unless --self-test is used")

        file_size, declared_input_hash, declared_output_hash, hunks = load_and_validate_patch()
        original = read_official_input(args.input)
        actual_input_hash = sha256(original)

        if len(original) != file_size or len(original) != EXPECTED_SIZE:
            raise PatchError(
                f"Unsupported firmware size: {len(original):,} bytes. "
                f"Expected {EXPECTED_SIZE:,} bytes."
            )
        if actual_input_hash != declared_input_hash.hex() or actual_input_hash != OFFICIAL_SHA256:
            raise PatchError(
                "This is not the exact supported Creative Stage SE v1001 firmware.\n"
                "No output was written.\n\n"
                f"Expected SHA-256: {OFFICIAL_SHA256}\n"
                f"Actual SHA-256:   {actual_input_hash}\n\n"
                "Do not use firmware for Stage SE mini or another Creative model."
            )

        patched = apply_patch(original, hunks)
        actual_output_hash = sha256(patched)
        if actual_output_hash != declared_output_hash.hex() or actual_output_hash != PATCHED_SHA256:
            raise PatchError(
                "Patched output failed checksum validation. No output was written.\n"
                f"Expected: {PATCHED_SHA256}\nActual:   {actual_output_hash}"
            )

        output = args.output or default_output_path(args.input)
        write_atomically(output, patched, args.force)

        print("Patch completed successfully")
        print(f"Model:  {SUPPORTED_MODEL}")
        print("Change: All 12 embedded prompts reduced to 14.8651% amplitude")
        print(f"Output: {output.resolve()}")
        print(f"SHA-256: {actual_output_hash}")
        print()
        print("IMPORTANT: This is unofficial firmware. Read README.md before installing.")
        return 0
    except PatchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except (OSError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
