# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.

import rpk
import json
import urllib.request
import urllib.error
from unittest.mock import MagicMock, patch
from pathlib import Path


def test_list_defs_success(capsys):
    """Test standard success path with mocked online fetching."""
    
    mock_response_content = json.dumps({
        "skills": [
            {"id": "test_skill_1", "description": "Description 1"},
            {"id": "test_skill_2", "description": "Description 2"}
        ]
    }).encode('utf-8')

    mock_response = MagicMock()
    mock_response.read.return_value = mock_response_content
    mock_response.__enter__.return_value = mock_response

    with patch('urllib.request.urlopen', return_value=mock_response):
        # We also need to patch open/Path to avoid writing to real user home during test
        with patch('builtins.open', new_callable=MagicMock) as mock_open:
            with patch.object(Path, 'mkdir') as mock_mkdir:
                rpk.main(['list-defs'])
    
    captured = capsys.readouterr()
    
    assert "Available Skill Definitions" in captured.out
    assert "test_skill_1" in captured.out
    assert "Description 1" in captured.out
    assert "test_skill_2" in captured.out


def test_list_defs_offline_with_cache(capsys):
    """Test offline behavior when cache exists."""
    
    mock_cache_content = json.dumps({
        "skills": [
            {"id": "cached_skill", "description": "Cached Description"}
        ]
    })

    # Simulate network error
    with patch('urllib.request.urlopen', side_effect=urllib.error.URLError("Offline")):
        # Simulate cache file existence and content
        with patch.object(Path, 'exists', return_value=True):
             with patch('builtins.open', new_callable=MagicMock) as mock_open:
                mock_file = MagicMock()
                mock_file.__enter__.return_value = mock_file
                mock_file.read.return_value = mock_cache_content
                # json.load reads from the file object
                with patch('json.load', return_value=json.loads(mock_cache_content)):
                    rpk.main(['list-defs'])

    captured = capsys.readouterr()
    assert "cached_skill" in captured.out
    assert "Cached Description" in captured.out


def test_list_defs_offline_no_cache(capsys):
    """Test offline behavior when no cache exists."""
    
    # Simulate network error
    with patch('urllib.request.urlopen', side_effect=urllib.error.URLError("Offline")):
        # Simulate NO cache file
        with patch.object(Path, 'exists', return_value=False):
             with patch('builtins.open', new_callable=MagicMock):
                try:
                    rpk.main(['list-defs'])
                except SystemExit:
                    pass # Expected as main catches exception and exits
    
    captured = capsys.readouterr()
    # Expect error message
    assert "Error" in captured.out
    assert "Offline" in captured.out
