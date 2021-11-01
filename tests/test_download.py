import os

from gdownplus.download import download


def test_download():
    url = "https://raw.githubusercontent.com/wkentaro/gdownplus/3.1.0/gdownplus/__init__.py"  # NOQA
    output = "/tmp/gdownplus_r"

    # Usage before https://github.com/wkentaro/gdownplus/pull/32
    assert download(url, output, quiet=False) == output
    os.remove(output)
