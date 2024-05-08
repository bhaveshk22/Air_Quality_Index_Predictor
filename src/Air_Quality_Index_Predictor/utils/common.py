import os
from box.exceptions import BoxValueError
import yaml
from Air_Quality_Index_Predictor.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any,Callable
from functools import wraps

breakpoints_dict = {
    "PM2.5": [0, 30, 60, 90, 120, 250],
    "PM10": [0, 50, 100, 250, 350, 430],
    "O3": [0, 50, 100, 168, 208, 748],
    "CO": [0, 1, 2, 10, 17, 34],
    "NO2": [0, 40, 80, 180, 280, 400],
    "SO2": [0, 40, 80, 380, 800, 1600]
}

def ensure_annotations(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper

@ensure_annotations
def get_subindex(x: float, breakpoints: list) -> float:
    if breakpoints[0] == 0:
        return 0.0  # Return 0 if the first breakpoint is 0 to avoid division by zero
    if x <= breakpoints[0]:
        return x * 50 / breakpoints[0]
    elif x <= breakpoints[1]:
        return 50 + (x - breakpoints[0]) * 50 / (breakpoints[1] - breakpoints[0])
    elif x <= breakpoints[2]:
        return 100 + (x - breakpoints[1]) * 100 / (breakpoints[2] - breakpoints[1])
    elif x <= breakpoints[3]:
        return 200 + (x - breakpoints[2]) * 100 / (breakpoints[3] - breakpoints[2])
    elif x <= breakpoints[4]:
        return 300 + (x - breakpoints[3]) * 100 / (breakpoints[4] - breakpoints[3])
    elif x > breakpoints[4]:
        return 400 + (x - breakpoints[4]) * 100 / (breakpoints[5] - breakpoints[4])
    else:
        return 0


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")