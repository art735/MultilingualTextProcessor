# Асинхронная функция для печати текущего времени
import asyncio
import time


# Запуск асинхронной функции
def run(callback):
    asyncio.run(_call_with_time_logging(callback))


# Асинхронная функция для вызова синхронного метода с печатью времени до и после
async def _call_with_time_logging(callback):
    start_time = time.time()
    await print_start_time(start_time)

    # Вызов синхронного метода
    callback()

    end_time = time.time()
    elapsed_time = end_time - start_time
    await print_end_time(end_time, elapsed_time)


# # Асинхронная функция для печати текущего времени
# async def _print_current_timestamp(time):
#     print(time.strftime("%H:%M:%S"))

async def print_start_time(start_time):
    # print(f"Start time: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    print(f"{time.strftime('%H:%M:%S', time.localtime(start_time))}")


async def print_end_time(end_time, elapsed_time):
    end_time_msg = f"{time.strftime('%H:%M:%S', time.localtime(end_time))}"

    if elapsed_time < 60:
        # print(f"Elapsed time: {elapsed_time:.2f} seconds")
        elapsed_time_msg = f'{int(elapsed_time)} sec'
    else:
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        # print(f"Elapsed time: {minutes} min and {seconds:.2f} sec")
        elapsed_time_msg = f'{minutes} min {int(seconds)} sec'

    print(f'{end_time_msg} (elapsed: {elapsed_time_msg})')
