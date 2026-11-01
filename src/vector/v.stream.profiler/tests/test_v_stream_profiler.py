"""Tests for v.stream.profiler."""

import pytest
from grass.exceptions import CalledModuleError
from grass.tools import ToolError


def test_downstream_profile_default(tmp_path, tools):
    """Test downstream profile generation without smoothing window."""
    orig_file = tmp_path / "orig.csv"
    tools.v_stream_profiler(
        cat=1,
        streams="streams",
        elevation="dem",
        outstream="out_default",
        outfile_original=str(orig_file),
    )

    info = tools.v_info(map="out_default", flags="t", format="json")
    assert info["lines"] > 0

    assert orig_file.exists()
    content = orig_file.read_text()
    assert len(content.strip().splitlines()) > 1


def test_downstream_profile_with_window(tmp_path, tools):
    """Test downstream profile generation with smoothing window."""
    orig_file = tmp_path / "orig_window.csv"
    smoothed_file = tmp_path / "smoothed.csv"
    tools.v_stream_profiler(
        cat=1,
        streams="streams",
        elevation="dem",
        accumulation="accum",
        slope="slope",
        window=20,
        outstream="out_window",
        outfile_original=str(orig_file),
        outfile_smoothed=str(smoothed_file),
    )

    assert orig_file.exists()
    assert smoothed_file.exists()
    assert len(orig_file.read_text().strip().splitlines()) > 1
    assert len(smoothed_file.read_text().strip().splitlines()) > 1


def test_upstream_direction_not_implemented(tools):
    """Test that upstream direction raises an error as not yet implemented."""
    with pytest.raises((CalledModuleError, ToolError)):
        tools.v_stream_profiler(
            cat=1,
            streams="streams",
            direction="upstream",
        )
