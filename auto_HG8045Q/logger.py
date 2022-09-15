from datetime import datetime


def log(log_type: str, message: str) -> None:
    time_stamp = _get_time()
    print(f'[{log_type}] {message} - {time_stamp}')


def _get_time() -> str:
    now = datetime.now()
    return now.strftime('%H:%M:%S')
