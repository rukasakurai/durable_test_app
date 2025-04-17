import logging
import time

def main(name: str) -> str:
    logging.info(f"Hello, {name}!")
    time.sleep(1)  # Wait for 1 second
    return f"Hello, {name}!"
