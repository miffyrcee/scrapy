from pathlib import Path

import ffmpeg


def process():
    p = Path()
    fns = p.glob('*.ts')
    fns = list(map(lambda fn: str(fn), fns))
    fns = sorted(fns, key=lambda fn: int(fn.split('-')[1]))
    return fns


def convert_to_mp4(fns):
    streams = list()
    for f in fns:
        streams.append(ffmpeg.input(f))
    conn = ffmpeg.concat(*streams)

    out = ffmpeg.output(conn, 'output.mp4')
    out.run()


if __name__ == "__main__":
    try:
        fns = process()
        convert_to_mp4(fns)
    except Exception:
        pass
