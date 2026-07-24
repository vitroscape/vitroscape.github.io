#!/usr/bin/env python3
"""Transcode grotte_1.mp4 (AV1 67Mbps) -> H.264 via PyAV(dav1d) decode + ffmpeg(x264) encode."""
import subprocess, sys
import av
import imageio_ffmpeg

SRC = '.review/video-backup/grotte_1.mp4'
DST = 'Immersion_Rupestre/assets/grotte_1.mp4'
FF  = imageio_ffmpeg.get_ffmpeg_exe()

container = av.open(SRC)
vs = container.streams.video[0]
W, H, FPS = vs.width, vs.height, 30

cmd = [FF, '-y',
       '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
       '-c:v', 'libx264', '-crf', '26', '-preset', 'medium',
       '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', DST]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

n = 0
try:
    for frame in container.decode(vs):
        f = frame.reformat(W, H, 'yuv420p')
        proc.stdin.write(f.to_ndarray().tobytes())
        n += 1
finally:
    proc.stdin.close()
rc = proc.wait()
print(f'frames: {n}, encoder rc: {rc}')
sys.exit(rc)
