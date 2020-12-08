import typer
from tqdm import tqdm
from time import sleep
from library.log import get_logger

logger = get_logger(__name__)


def main(required_arg: str, optional_arg: str = None) -> None:
    logger.info(f"Hello! required_arg = {required_arg}, optional_arg = {optional_arg}")

    for i in tqdm(range(5)):
        sleep(0.1)


if __name__ == "__main__":
    typer.run(main)
