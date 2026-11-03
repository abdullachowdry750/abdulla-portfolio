import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or has no columns.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    logger.info("Starting CSV ingestion: %s", path.name)

    try:
        dataframe = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"CSV file is empty: {path}") from exc

    if dataframe.empty:
        raise ValueError(f"CSV contains no data rows: {path}")

    if len(dataframe.columns) == 0:
        raise ValueError(f"CSV contains no columns: {path}")

    logger.info(
        "CSV ingestion completed: file=%s rows=%s columns=%s",
        path.name,
        len(dataframe),
        len(dataframe.columns),
    )

    return dataframe
