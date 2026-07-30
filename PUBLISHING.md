# Publishing checklist

Recommended repository settings for **blazer5000/creative-stage-se-quieter-startup-sounds**.

## Create the repository

- Repository name: `creative-stage-se-quieter-startup-sounds`
- Visibility: Public
- Do not initialise it with another README, licence or `.gitignore`; those are already included.

Suggested description:

> Patch for Creative Stage SE (MF8410) that reduces the loud startup, power-on and voice-prompt volume to 14.865% without redistributing Creative firmware.

Suggested topics:

- `creative-stage-se`
- `creative`
- `soundbar`
- `mf8410`
- `firmware-patch`
- `startup-sound`
- `power-on-sound`
- `voice-prompts`
- `volume-fix`
- `python`

## Upload

### GitHub website

1. Create the empty public repository.
2. Choose **uploading an existing file**.
3. Upload all files and folders from this package, preserving the folders.
4. Commit to `main` with: `Publish quieter Stage SE prompt patch`

GitHub's web uploader may be awkward for nested folders. GitHub Desktop is easier:

1. Create the empty repository on GitHub.
2. In GitHub Desktop, choose **File → Add local repository** or initialise this folder.
3. Commit all files.
4. Publish/push to the empty repository.

## Release

Create a release after the repository is live:

- Tag: `v1.0.0`
- Title: `v1.0.0 – Quieter Creative Stage SE startup and voice prompts`

Suggested release text:

> First tested release for Creative Stage SE model MF8410 using official firmware v1001. All 12 embedded startup and status prompts are reduced to 14.8651% amplitude. The repository does not include Creative firmware; download the official package from Creative and run the included patcher.

Do not attach the complete official or patched `ota.bin`, and do not attach extracted MP3 files.

## Improve discoverability

- Keep the repository public.
- Add all suggested GitHub topics.
- Put the exact product and model in the description.
- Create the `v1.0.0` release.
- Share the repository in relevant Creative support/community discussions where self-promotion is permitted.
- Use descriptive issue and discussion titles such as “Creative Stage SE startup sound too loud”.
- Enable Issues so owners can report whether their MF8410 revision worked.

Search engines normally discover public GitHub repositories automatically. The repository title, description, headings and repeated natural-language problem terms in README are intentionally written for relevant searches rather than keyword stuffing.
