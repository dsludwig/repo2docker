"""
Test if the subdirectory is correctly navigated to
"""
import logging
from os.path import abspath, dirname

import pytest
from repo2docker.app import Repo2Docker

# This is the path to the repo2docker git repository that this file exists in.
repo_path = dirname(dirname(abspath(__file__)))


def test_subdir(run_repo2docker):
    argv = ['--subdir', 'tests/conda/simple', repo_path]
    run_repo2docker(argv)


def test_subdir_invalid(caplog):
    caplog.set_level(logging.INFO, logger='Repo2Docker')

    app = Repo2Docker()
    argv = ['--subdir', 'tests/conda/invalid', repo_path]
    app.initialize(argv)
    app.debug = True
    app.run = False
    with pytest.raises(SystemExit) as excinfo:
        app.start()  # Just build the image and do not run it.

    # The build should fail
    assert excinfo.value.code == 1

    # Can't get this to record the logs?
    # assert caplog.text == "Subdirectory tests/conda/invalid does not exist"
