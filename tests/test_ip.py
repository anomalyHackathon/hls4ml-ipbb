import pytest
from hls4ml_ipbb import Project


def test_project_file_not_found():
    with pytest.raises(FileNotFoundError):
        Project('rtjiogjogjoier12', backend=None)
