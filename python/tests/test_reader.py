import pytest
from uatk_spc.reader import Reader, filepath_to_path_and_region, is_parquet, is_protobuf

TEST_URL_PB = (
    "https://ramp0storage.blob.core.windows.net/test-spc-output/test_region.pb.gz"
)
TEST_URL_PQ = (
    "https://ramp0storage.blob.core.windows.net/test-spc-output/test_region.tar.gz"
)


def test_is_parquet():
    assert is_parquet(TEST_URL_PQ)
    assert not is_parquet(TEST_URL_PB)


def test_is_protobuf():
    assert is_protobuf(TEST_URL_PB)
    assert not is_protobuf(TEST_URL_PQ)


@pytest.mark.parametrize("filepath", [TEST_URL_PB, TEST_URL_PQ])
def test_filepath_to_path_and_region(filepath):
    _, region = filepath_to_path_and_region(filepath)
    assert region == "test_region"


@pytest.mark.parametrize("filepath", [TEST_URL_PB, TEST_URL_PQ])
def test_reader(filepath):
    spc = Reader(filepath=filepath)
    print(spc.people)
    assert spc.people.shape[0] == 4991


def test_merge_people_and_time_use_diaries():
    spc = Reader(filepath=TEST_URL_PQ)
    merged = spc.merge_people_and_time_use_diaries(
        {"health": ["bmi"], "demographics": ["age_years"]}, diary_type="weekday_diaries"
    )
    assert merged.shape == (197_397, 30)


def test_merge_people_and_households():
    spc = Reader(filepath=TEST_URL_PQ)
    merged = spc.merge_people_and_households()
    assert merged.shape == (4991, 17)
