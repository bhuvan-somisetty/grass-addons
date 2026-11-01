"""Fixtures for v.stream.profiler tests."""

import os
import pytest

import grass.script as gs
from grass.tools import Tools

STREAM_ASCII = """L 2 1
 50 100
 50 50
 1 1
L 2 1
 50 50
 50 0
 1 2
"""


@pytest.fixture(scope="module")
def session(tmp_path_factory):
    """Temporary GRASS project with synthetic DEM and stream network."""
    tmp = tmp_path_factory.mktemp("v_stream_profiler")
    project = os.path.join(tmp, "project")
    gs.create_project(project)
    with gs.setup.init(project) as session:
        tools = Tools(session=session)
        tools.g_region(n=100, s=0, e=100, w=0, res=1)
        tools.r_mapcalc(expression="dem = 100.0 - y()")
        tools.r_mapcalc(expression="accum = 10.0 + x()")
        tools.r_mapcalc(expression="slope = 0.05")

        stream_file = tmp_path_factory.mktemp("stream") / "stream.txt"
        stream_file.write_text(STREAM_ASCII)
        tools.v_in_ascii(
            input=str(stream_file),
            output="streams",
            format="standard",
            flags="n",
        )
        tools.v_db_addtable(
            map="streams",
            columns="cat integer, fromstream integer, tostream integer",
        )
        tools.v_db_update(map="streams", column="fromstream", value="1", where="cat=1")
        tools.v_db_update(map="streams", column="tostream", value="2", where="cat=1")
        tools.v_db_update(map="streams", column="fromstream", value="2", where="cat=2")
        tools.v_db_update(map="streams", column="tostream", value="0", where="cat=2")

        yield session


@pytest.fixture
def tools(session):
    return Tools(session=session, capture_stderr=True, consistent_return_value=True)
