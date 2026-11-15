# Udemie product tour: Microsoft Store trailers

The homepage product tour of Udemie 4.3.1 (the "Watch the tour" button on https://www.udemie.study),
packaged for the Microsoft Store listing. The film was recorded from the real desktop app and
edited with Remotion; its source lives in the private website repository (`video/`,
`docs/homepage-tour/`, PR zenderock/udemie-website#136).

| File | What it is |
| --- | --- |
| `udemie-tour-en-store.mp4` | Trailer, English captions. MP4, H.264, 1920x1080, 30 fps, 1:25, silent AAC-LC 48 kHz stereo track |
| `udemie-tour-fr-store.mp4` | Trailer, French captions. Same format |
| `udemie-tour-en-thumbnail.png` | Trailer thumbnail (cover), PNG 1920x1080, English title card |
| `udemie-tour-fr-thumbnail.png` | Trailer thumbnail (cover), PNG 1920x1080, French title card |
| `SHA256SUMS` | Checksums of the four files |

## For the Store listing

- Captions are burned into the image: use the EN trailer for English listings and the FR
  trailer for French ones, each with its thumbnail of the same language.
- Partner Center expects MP4 or MOV, H.264, 1920x1080 and a 1920x1080 PNG thumbnail per
  trailer. The film itself has no sound; the silent AAC track is there because the Store
  specifications expect an audio stream.
- Microsoft recommends trailers of 60 seconds or less; this one runs 85 seconds.
- The same films without the audio track are served by the website:
  `https://www.udemie.study/videos/udemie-tour-en.mp4` and `.../udemie-tour-fr.mp4`.

These files are assets only: no workflow in this repository reads them.
