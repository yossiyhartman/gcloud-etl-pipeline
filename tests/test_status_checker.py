import datetime as dt
from unittest.mock import patch

import polars as pl
import pytest

from gcp_pipeline.file_status_log import FileStatusLog


@pytest.fixture
def sample_current_status():
    return pl.DataFrame(
        {
            "name": ["file1.json", "file2.json", "file3.json"],
            "updated": [
                dt.datetime(2024, 1, 1),
                dt.datetime(2024, 1, 2),
                dt.datetime(2024, 1, 3),
            ],
        }
    )


@pytest.fixture
def sample_latest_status():
    return pl.DataFrame(
        {
            "name": ["file1.json", "file2.json"],
            "updated": [
                dt.datetime(2024, 1, 1),  # unchanged
                dt.datetime(2023, 12, 31),  # outdated
            ],
        }
    )


# -----------------------------------------------------------------------------
# get_latest_file_status
# -----------------------------------------------------------------------------


@patch("polars.read_delta")
def test_get_latest_file_status_success(mock_read_delta, sample_latest_status):
    mock_read_delta.return_value = sample_latest_status

    log = FileStatusLog("bucket", "path")
    result = log.get_latest_file_status()

    assert result.equals(sample_latest_status)


# -----------------------------------------------------------------------------
# get_files_to_update
# -----------------------------------------------------------------------------


def test_get_files_to_update(sample_current_status, sample_latest_status):
    log = FileStatusLog("bucket", "path")

    result = log.get_files_to_update(
        latest_status=sample_latest_status,
        cur_status=sample_current_status,
    )

    # file2 updated, file3 new
    assert set(result) == {"file2.json", "file3.json"}


def test_get_files_to_update_no_changes(sample_latest_status):
    log = FileStatusLog("bucket", "path")

    result = log.get_files_to_update(
        latest_status=sample_latest_status,
        cur_status=sample_latest_status,
    )

    assert result == []


def test_get_files_to_update_all_new(sample_current_status):
    log = FileStatusLog("bucket", "path")

    empty = pl.DataFrame(schema={"name": pl.String, "updated": pl.Datetime})

    result = log.get_files_to_update(
        latest_status=empty,
        cur_status=sample_current_status,
    )

    assert set(result) == set(sample_current_status["name"].to_list())


# -----------------------------------------------------------------------------
# update_log
# -----------------------------------------------------------------------------


@patch("polars.DataFrame.write_delta")
def test_update_log_calls_write(mock_write_delta, sample_current_status):
    log = FileStatusLog("bucket", "path")

    log.update_log(sample_current_status)

    mock_write_delta.assert_called_once()
