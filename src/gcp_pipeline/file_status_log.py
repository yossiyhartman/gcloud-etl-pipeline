import logging

import polars as pl

logger = logging.getLogger(__name__)


class FileStatusLog:
    """Handles reading, comparing, and updating file status logs stored in Delta format."""

    def __init__(self, bucket_name: str, path: str) -> None:
        self.path = f"gs://{bucket_name}/{path}"

    def get_latest_file_status(self) -> pl.DataFrame:
        """Load the latest file status log."""
        try:
            df = pl.read_delta(self.path)

            self._validate_schema(df)
            return df

        except Exception:
            logger.error("Failed to read file status log. Assume no earlier statuses are logged")

        return self._empty_status_df()

    def get_files_to_update(self, latest_status: pl.DataFrame, cur_status: pl.DataFrame) -> list[str]:
        """Determine which files are new or updated."""

        self._validate_schema(cur_status)
        self._validate_schema(latest_status)

        joined = cur_status.join(latest_status, on="name", how="left", suffix="_latest")
        filtered = joined.filter(pl.col("updated").ne_missing(pl.col("updated_latest")))
        files = filtered["name"].to_list()

        return files

    def update_log(self, cur_status: pl.DataFrame) -> None:
        """Overwrite the file status log with current state."""

        self._validate_schema(cur_status)

        try:
            cur_status.write_delta(self.path, mode="overwrite")
            logger.info("File status log updated at %s", self.path)

        except Exception as e:
            logger.error("Failed to update file status log: %s", e)
            raise

    @staticmethod
    def _empty_status_df() -> pl.DataFrame:
        """Return an empty status DataFrame with correct schema."""
        return pl.DataFrame(schema={"name": pl.String, "updated": pl.Datetime(time_zone="UTC")})

    @staticmethod
    def _validate_schema(df: pl.DataFrame) -> None:
        """Ensure required columns exist."""
        required_columns = {"name", "updated"}
        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(f"Missing required columns: {missing}")
