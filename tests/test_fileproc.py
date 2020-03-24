#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pytest
import tempfile
from urlchecker.core.fileproc import check_file_type, get_file_paths, collect_links_from_file, include_file, remove_empty, save_results


@pytest.mark.parametrize('file_path', ["tests/test_files/sample_test_file.md",
                                       "tests/test_files/sample_test_file.py"])
@pytest.mark.parametrize('file_types', [[".md", ".py"]])
def test_check_file_type(file_path, file_types):
    """
    test check file types
    """
    output = check_file_type(file_path, file_types)
    if not output:
        raise AssertionError

    # check for false
    output = check_file_type(file_path + ".nonesense", file_types)
    if output:
        raise AssertionError


@pytest.mark.parametrize('file_path', ["tests/test_files/sample_test_file.md",
                                       "tests/test_files/sample_test_file.py"])
@pytest.mark.parametrize('white_list_patterns', [["[.py]"], ["[.md]"], ["tests/test_file"]])
def test_include_files(file_path, white_list_patterns):
    """
    test if a file should be included based on patterns (using extension for test)
    """
    _, extension = os.path.splitext(file_path)
    expected = not extension in file_path
    result = include_file(file_path, white_list_patterns)

    # No files should be included for a global path pattern
    if "tests/test_file" in white_list_patterns:
        if result:
            raise AssertionError

    # Otherwise, the patterns should honor extension
    else:
        if result != expected:
            raise AssertionError

@pytest.mark.parametrize('base_path', ["tests/test_files"])
@pytest.mark.parametrize('file_types', [[".md", ".py"]])
def test_get_file_paths(base_path, file_types):
    """
    get path to all files under a give directory and its subfolders.

    Args:
        base_path   (str) : base path.
        file_types (list) : list of file extensions to accept.

    Returns:
        list of file paths.
    """
    file_paths = get_file_paths(base_path, file_types)
    expected_paths = [["tests/test_files/sample_test_file.md",
                       "tests/test_files/sample_test_file.py"],
                     ["tests/test_files/sample_test_file.py",
                      "tests/test_files/sample_test_file.md"]]
    # assert
    assert(file_paths in expected_paths)


@pytest.mark.parametrize('file_path', ["tests/test_files/sample_test_file.md",
                                       "tests/test_files/sample_test_file.md"])
def collect_links_from_file(file_path):
    """
    test links collerction function.
    """
    # read file content
    urls = collect_links_from_file()
    assert(len(url) == 3)


def test_remove_empty():
    """
    test that empty urls are removed
    """
    urls = ["notempty", "notempty", "", None]
    if len(remove_empty(urls)) != 2:
        raise AssertionError


def test_save_results():
    """
    test that saving results works.
    """
    check_results = {"failed": ["fail1", "fail2"], "passed": ["pass1", "pass2"]}
    output_csv = tempfile.NamedTemporaryFile(suffix=".csv", prefix="urlchecker-").name
    output_file = save_results(check_results, output_csv)
    if not os.path.exists(output_csv):
        raise AssertionError
