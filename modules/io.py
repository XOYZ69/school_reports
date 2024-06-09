import os
import time

from tqdm import tqdm

def copy_with_progress(src, dst, chunk_size=1024):
    total_size = os.path.getsize(src)
    progress_bar = tqdm(
        desc=time.ctime() + f' Copying [{src}]',
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    )

    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        while True:
            data = fsrc.read(chunk_size)
            if not data:
                break
            fdst.write(data)
            progress_bar.update(len(data))

    progress_bar.close()
