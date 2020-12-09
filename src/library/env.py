import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name, default=None) -> str:
    if os.getenv(name) is None and default is None:
        raise Exception(f"{name} environment variable is not set.")
    elif os.getenv(name) is None:
        return default
    else:
        return os.environ[name]


# def get_env_bool(name, default="False"):
#     val = get_env(name, str(default))
#     return bool(distutils.util.strtobool(val))
