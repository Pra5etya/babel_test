from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

import os, logging, atexit


def setup_logger():
    log_name = "record"
    log_dir = "logs"

    try:
        os.makedirs(log_dir, exist_ok = True)
    except Exception as e:
        print(f"Gagal membuat direktori '{log_dir}': {e}")

    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{log_dir}/{log_name}_{today_str}.log"

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding='utf-8',
            utc=False
        )

        formatter = logging.Formatter(
            "[%(asctime)s] [%(threadName)s:%(funcName)s] \t %(levelname)s: \t %(message)s"
        )
        handler.setFormatter(formatter)
        handler.suffix = "%Y-%m-%d"

        logger.addHandler(handler)

        # Fungsi ini akan dipanggil saat program keluar
        def write_exit_lines():
            handler.stream.write("\n")  # enter kosong
            handler.flush()

        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':   # log dimulai ketika restart
            boundary = "="  * 30

            logger.info(f"{boundary} LOGGER STARTING POINT {boundary} \n")
            logger.info("Flask is restarting...")
            logger.info("Log Start ... \n")

        # Daftarkan sekali saja
        atexit.register(write_exit_lines)

    return logger