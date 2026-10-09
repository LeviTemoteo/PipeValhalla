import logging
import sys
from pathlib import Path

log_dir = Path("~/.pipevalhalla").expanduser()
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "pipevalhalla.log"

def setup_logger():
    
    logger = logging.getLogger("PipeValhalla")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.ERROR)

    file_formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s:%(lineno)d) - %(message)s")

    file_handler.setFormatter(file_formatter)

    cli_handler = logging.StreamHandler(sys.stdout)
    cli_handler.setLevel(logging.INFO)

    cli_formatter = logging.Formatter("%(levelname)s: %(message)s")
    cli_handler.setFormatter(cli_formatter)

    return logger

logger = setup_logger()