# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. 
# Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы

import os
import time
import threading
from pathlib import Path
import requests
import multiprocessing
import aiohttp
import asyncio
import aiofiles

# многопоточность
task_dir = os.path.join(Path(__file__).resolve().parent, 'task_')

if not os.path.exists(task_dir):
    os.mkdir(task_dir)

BASE_DIR = os.path.join(task_dir, 'threads')

if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)

urls = [
    'https://i.imgur.com/vfiefI0.jpeg',
    'https://i.imgur.com/qcoE5I9.png',
    'https://i.imgur.com/VTWTeCF.png',
    'https://onrockwave.com/wp-content/uploads/2022/04/orw_071-1-350x250.jpg',
    'https://cloud4box.com/wp-content/uploads/python-300x161.jpg',
]

def download_image(url: str):
    response = requests.get(url)
    paths = url.replace('https://', '').split('/')
    dirname, filename = paths[0].replace('.', '_'), paths[-1]

    if not os.path.exists(os.path.join(BASE_DIR, dirname)):
        os.mkdir(os.path.join(BASE_DIR, dirname))

    with open(os.path.join(BASE_DIR, dirname, filename), 'wb') as f:
        f.write(response.content)

def main():
    threads: list[threading.Thread] = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=download_image, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f'Загрузка закончена {time.time() - start_time} секунд потрачено.')

# if __name__ == '__main__':
#     main()

# многопроцессорность
task_dir_2 = os.path.join(Path(__file__).resolve().parent, 'task_')

if not os.path.exists(task_dir_2):
    os.mkdir(task_dir_2)

BASE_DIR_2 = os.path.join(task_dir_2, 'processes')

if not os.path.exists(BASE_DIR_2):
    os.mkdir(BASE_DIR_2)

def download_image(url: str):
    response = requests.get(url)
    paths = url.replace('https://', '').split('/')
    dirname, filename = paths[0].replace('.', '_'), paths[-1]

    if not os.path.exists(os.path.join(BASE_DIR_2, dirname)):
        os.mkdir(os.path.join(BASE_DIR_2, dirname))

    with open(os.path.join(BASE_DIR_2, dirname, filename), 'wb') as f:
        f.write(response.content)


def main2():
    processes: list[multiprocessing.Process] = []

    start_time = time.time()

    for url in urls:
        process = multiprocessing.Process(target=download_image, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'Загрузка завершена {time.time() - start_time} секунд затрачено.')


# if __name__ == '__main__':
#     main2()
    
# асинхронность
task_dir_3 = os.path.join(Path(__file__).resolve().parent, 'task_')

if not os.path.exists(task_dir_3):
    os.mkdir(task_dir_3)

BASE_DIR_3 = os.path.join(task_dir_3, 'async')

if not os.path.exists(BASE_DIR_3):
    os.mkdir(BASE_DIR_3)

async def download_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            paths = url.replace('https://', '').split('/')
            dirname, filename = paths[0].replace('.', '_'), paths[-1]

            if not os.path.exists(os.path.join(BASE_DIR_3, dirname)):
                os.mkdir(os.path.join(BASE_DIR_3, dirname))

            async with aiofiles.open(
                os.path.join(BASE_DIR_3, dirname, filename), 'wb'
            ) as f:
                await f.write(await response.content.read())


async def main():
    tasks = []

    for url in urls:
        task = asyncio.ensure_future(download_image(url))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f'Загрузка завершена {time.time()- start_time} секунд затрачено.')