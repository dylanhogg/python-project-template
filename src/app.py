import typer
from tqdm import tqdm
from time import sleep
from library import log
from library import env

logger = log.get_logger(__name__)


def main(required_arg: str, optional_arg: str = None) -> None:
    python_path = env.get_env("PYTHONPATH", "not set")
    logger.info(f"Hello!\nrequired_arg = {required_arg}, optional_arg = {optional_arg}\npython_path = {python_path}")

    for i in tqdm(range(5)):
        sleep(0.1)


if __name__ == "__main__":
    typer.run(main)
