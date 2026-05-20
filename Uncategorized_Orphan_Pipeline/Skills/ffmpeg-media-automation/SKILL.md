---
name: ffmpeg-media-automation
description: >
  Comprehensive FFmpeg/FFprobe skill for all media automation tasks. Use when the user asks for
  video/audio conversion, trimming, resizing, padding, overlays, subtitles, thumbnails, GIFs,
  storyboards, slideshows, social-media crops, codec settings, CRF/preset tuning, stream mapping,
  GPU-accelerated encoding, batch processing, or troubleshooting media pipelines.
  Replaces: ffmpeg-video-editing, ffmpeg-format-conversion.
skill-author: Merged (rendi-api/ffmpeg-cheatsheet + benchflow-ai/skillsbench + AROS internal)
license: MIT
original-source: https://github.com/rendi-api/ffmpeg-cheatsheet
---

# FFmpeg Media Automation

Use this skill to produce reliable, explainable FFmpeg/FFprobe commands for media automation.

## Workflow

1. Identify the user's source media, desired output container/codec, target dimensions/duration, and whether quality, speed, or file size matters most.
2. Prefer the simplest command that meets the goal.
3. Use `-c copy` only when no filtering, re-encoding, precise trimming, subtitle burn-in, compression, or codec change is needed.
4. Use explicit stream mapping when multiple inputs or outputs are involved.
5. For commands with filters, quote the filter graph and name streams in `filter_complex` when it improves readability.
6. Include `-y` only when the user wants non-interactive overwrite behavior.
7. Validate command intent with `ffprobe` or a low-duration sample when practical.

## Codec Defaults & Presets

| Use Case | Command Flags |
|----------|--------------|
| Web-compatible MP4 | `-c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a aac -movflags +faststart` |
| High-quality archival H.264 | `-c:v libx264 -crf 17` or `-crf 18` |
| Smaller modern MP4 (HEVC) | `-c:v libx265 -crf 24 -vtag hvc1 -c:a aac` |
| WebM/VP9 | `-c:v libvpx-vp9 -crf 15 -b:v 0 -c:a libopus` |
| Preserve audio when safe | `-c:a copy` |
| Force square pixels | `setsar=1:1` after scale/pad/crop |
| Playback compatibility | `format=yuv420p` or `-pix_fmt yuv420p` |
| GPU (NVIDIA) H.264 | `-c:v h264_nvenc` |
| GPU (NVIDIA) H.265 | `-c:v hevc_nvenc` |
| GPU (Intel QSV) | `-init_hw_device qsv=hw -filter_hw_device hw -c:v h264_qsv` |

### CRF Guidance
- CRF 0–51 for libx264 (23 default; 17–18 visually lossless; lower = better; +6 ≈ half bitrate)
- CRF 0–63 for libvpx-vp9 (31 default for 1080p; 15–35 recommended range)
- Use `-b:v 0` with VP9 CRF to enable constant-quality mode

### Encoding Speed vs Quality
- `-preset veryslow` → best compression, slowest encode (web archival)
- `-preset slow` → good default for quality
- `-preset ultrafast` → fastest encode, largest file (real-time/testing)

## Common Command Patterns

### Inspect Media
```bash
ffprobe -hide_banner -show_streams -show_format input.mp4
```

### Remux Without Re-encoding
```bash
ffmpeg -i input.mp4 -c copy output.mkv   # MP4→MKV
ffmpeg -i input.mp4 -c copy output.mov   # MP4→MOV
```

### Resize and Pad to Vertical 1080×1920
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1:1" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a aac -movflags +faststart \
  output.mp4
```
- `scale=w=X:h=-2` lets FFmpeg pick height while forcing even dimensions
- `force_original_aspect_ratio=decrease` auto-shrinks to fit

### Frame-Accurate Trim
Use output seeking and re-encode for reliable exact cuts:
```bash
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:25 \
  -c:v libx264 -crf 18 -preset slow -c:a aac output_trimmed.mp4
```
Use input seeking (before `-i`) only when speed matters more than accuracy.

### Replace Audio
```bash
ffmpeg -i input.mp4 -i music.mp3 \
  -map 0:v -map 1:a -shortest -c:v copy -c:a aac output.mp4
```

### Mix Background Music Under Original Audio
```bash
ffmpeg -i input.mp4 -i music.mp3 \
  -filter_complex "[1:a]volume=0.2[bgm];[0:a][bgm]amix=inputs=2:duration=shortest[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -shortest output.mp4
```

### Extract Audio
```bash
# Quick MP3 extraction
ffmpeg -i input.mp4 output.mp3

# Controlled: mono, 16kHz, 48kbps
ffmpeg -i input.mp4 -ar 16000 -ab 48k -codec:a libmp3lame -ac 1 output.mp3

# Lossless copy (no re-encode)
ffmpeg -i input.mp4 -map 0:a:0 -acodec copy output.aac
```

### Overlay Logo for a Time Range
```bash
ffmpeg -i input.mp4 -i logo.png \
  -filter_complex "overlay=x=(main_w-overlay_w)/8:y=(main_h-overlay_h)/8:enable='gte(t,1)*lte(t,7)'" \
  -c:v libx264 -crf 18 -preset slow -c:a copy output.mp4
```

### Overlay with Controlled Transparency
```bash
ffmpeg -i input.mp4 -i logo.png \
  -filter_complex "[1:v]format=argb,geq='p(X,Y)':a='0.5*alpha(X,Y)'[v1];[0:v][v1]overlay=..." \
  -c:v libx264 -c:a copy output.mp4
```

### Burn Subtitles
```bash
ffmpeg -i input.mp4 \
  -vf "subtitles=subtitles.srt:fontsdir=.:force_style='FontName=Poppins,FontSize=24,PrimaryColour=&HFFFFFF'" \
  -c:v libx264 -crf 18 -preset slow -c:a copy output.mp4
```
- Colors are `&HBBGGRR` (or `&HAABBGGRR` with alpha)
- For custom subtitle appearances, use ASS format
- Pixel-perfect: render opaque images and overlay them

### Add Soft Subtitle Track
```bash
ffmpeg -i input.mp4 -i subtitles.srt \
  -c copy -c:s srt -disposition:s:0 default output.mkv
```

### Text Overlay with Timed Fade-in
```bash
ffmpeg -i input.mp4 -vf "drawtext=text='Hello':x=50:y=100:fontsize=80:fontcolor=black:alpha='if(gte(t,1)*lte(t,3),(t-1)/2,1)':box=1:boxcolor=#6bb666@0.6:boxborderw=7:enable='gte(t,1)'" \
  -c:v libx264 output.mp4
```
- Prefer `textfile=` over inline text to avoid shell escaping issues

### Speed Change (Without Audio Distortion)
```bash
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]setpts=PTS/1.5[v];[0:a]atempo=1.5[a]" \
  -map "[v]" -map "[a]" output.mp4
```

### Jump Cuts
```bash
ffmpeg -i input.mp4 \
  -vf "select='between(t,0,5.7)+between(t,11,18)',setpts=N/FRAME_RATE/TB" \
  -af "aselect='between(t,0,5.7)+between(t,11,18)',asetpts=N/SR/TB" \
  output.mp4
```

### Thumbnail Extraction
```bash
# Single frame at 7 seconds
ffmpeg -i input.mp4 -ss 00:00:07 -frames:v 1 -q:v 2 thumbnail.jpg

# Scene change detection thumbnail
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)'" -frames:v 1 -q:v 2 thumbnail.jpg
```

### GIF from Video
```bash
ffmpeg -i input.mp4 \
  -vf "select='gt(trunc(t/2),trunc(prev_t/2))',setpts='PTS*0.1',scale=trunc(oh*a/2)*2:320:force_original_aspect_ratio=decrease,pad=trunc(oh*a/2)*2:320:-1:-1" \
  -loop 0 -an output.gif
```

### Image to Video (Loop + Fade)
```bash
ffmpeg -loop 1 -t 10 -i image.png -i audio.mp3 \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1:color=black,setsar=1,fade=t=in:st=0:d=1,format=yuv420p" \
  -c:v libx264 -c:a aac -shortest output.mp4
```

### Slideshow with Crossfade (xfade)
```bash
ffmpeg -loop 1 -t 5 -i img1.png -loop 1 -t 5 -i img2.png -i audio.mp3 \
  -filter_complex "[0:v]format=yuv420p,fade=t=in:st=0:d=0.5,setpts=PTS-STARTPTS[v0];[1:v]format=yuv420p,fade=t=out:st=4.5:d=0.5,setpts=PTS-STARTPTS[v1];[v0][v1]xfade=transition=fade:duration=0.5:offset=4.5,format=yuv420p[v]" \
  -map "[v]" -map 2:a -c:v libx264 -c:a aac -shortest output.mp4
```

### Ken Burns Effect (Zoom Pan)
Use `zoompan` filter with high-res `scale=8000:-1` to avoid jitter:
```bash
# zoom=1+0.005 per frame, centered, 100 frames at 25fps = 4 seconds
-vf "scale=8000:-1,zoompan=z='zoom+0.005':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=100:s=1920x1080:fps=25,trim=duration=4,format=yuv420p,setpts=PTS-STARTPTS"
```

### Storyboard / Tiled Thumbnails
```bash
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)',scale=640:480,tile=2x2" -frames:v 1 storyboard.jpg
```

### Concat Intro + Main + Outro with Background Music
```bash
ffmpeg -i intro.mp4 -i main.mp4 -i outro.mp4 -i bgm.mp3 \
  -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1[iv];...;concat=n=3:v=1:a=1[cv][ca];[3:a]volume=0.1,...amix=inputs=2:duration=first[fa]" \
  -map "[cv]" -map "[fa]" -c:v libx264 -c:a aac -shortest output.mp4
```
- Normalize all inputs: same fps, format, SAR, audio sample format
- Use `aformat=sample_fmts=fltp:channel_layouts=stereo` for consistent audio

### Stack Videos Vertically/Horizontally
```bash
# Vertical stack
-filter_complex "[0:v]scale=720:-2,pad=720:640[top];[1:v]scale=720:-2,pad=720:640[bot];[top][bot]vstack=inputs=2:shortest=1[v]"
```

### Video Cropping for Social Media (Split + Trim + Crop)
```bash
ffmpeg -i input.mp4 -vf "split=3[1][2][3];[1]trim=0:4.5,setpts=PTS-STARTPTS,crop=...,scale=720:1080,setsar=1[1];..." \
  -c:v libx264 -c:a copy output_cropped.mp4
```

### Audio Crossfade
```bash
ffmpeg -i track1.mp3 -i track2.mp3 \
  -filter_complex "[0:0][1:0]acrossfade=d=3:c1=exp:c2=qsin" \
  -c:a libmp3lame -q:a 2 output.mp3
```

### Dynamic Audio Normalization
```bash
-filter_complex "amix=inputs=2:duration=longest,pan=mono|c0=.5*c0+.5*c1,dynaudnorm"
```

### Batch Conversion
```bash
for f in *.mkv; do ffmpeg -i "$f" -c copy "${f%.mkv}.mp4"; done
for f in *.avi; do ffmpeg -i "$f" -c:v libx264 -c:a aac "${f%.avi}.mp4"; done
```

### Batch Segment Removal (Python)
For removing many short segments (pauses, filler), see the `video-processor` skill which provides a full Python pipeline.

## Gotchas

- **`-c copy` cannot apply filters** and is not frame-accurate for most cuts.
- **`-ss` before `-i`** is fast but approximate (keyframe-seeking); **`-ss` after `-i`** is slower but frame-accurate. For trimming, always use output seeking and re-encode unless speed is paramount.
- **MP4 playback** in QuickTime and browsers often needs `yuv420p` for H.264 output.
- **`-movflags +faststart`** moves moov atom to front for web streaming — use for web-hosted MP4/MOV/M4A.
- **Stream mapping**: `[0:v]` = first input's video, `[1:a]` = second input's audio, `-map` chooses output streams.
- **Escaping filter expressions** is shell-sensitive. Prefer single quotes inside double-quoted filter graphs.
- **`drawtext` with special characters** is fragile; prefer `textfile=` for user-supplied text.
- **Burned subtitles require re-encoding**; soft subtitle tracks can use stream copy.
- **Apple devices + H.265**: use `-vtag hvc1` to fix AirDrop/QuickTime issues.
- **`-shortest`** controls final output duration; `duration=shortest` in `amix` controls audio mixing duration. Both are often needed together.
- **concat filter requires uniform inputs**: same fps, pixel format, SAR, and audio format. Normalize with `fps=30,format=yuv420p,setsar=1` and `aformat=sample_fmts=fltp:channel_layouts=stereo`.
- **zoompan jitter**: pre-upscale with `scale=8000:-1` before zoompan to avoid the known jitter bug.
- **`vsync`** is deprecated — use `-fps_mode` in newer FFmpeg versions.
- **Verify faststart**: `ffprobe -v trace -i video.mp4` — look for `type:'moov'` near the beginning.

## When More Depth Is Needed

Load `references/command-patterns.md` for additional decision rules and advanced social-media cropping patterns.
