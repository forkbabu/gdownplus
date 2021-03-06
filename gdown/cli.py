from __future__ import print_function

import argparse
import re
import sys

import pkg_resources
import six

from .download import download
from .download_folder import download_folder

distribution = pkg_resources.get_distribution("gdownplus")


class _ShowVersionAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        kwargs["nargs"] = 0
        self.version = kwargs.pop("version")
        super(self.__class__, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(
            "gdownplus {ver} at {pos}".format(
                ver=self.version, pos=distribution.location
            )
        )
        parser.exit()


def file_size(argv):
    if argv is not None:
        m = re.match(r"([0-9]+)(GB|MB|KB|B)", argv)
        if not m:
            raise TypeError
        size, unit = m.groups()
        size = float(size)
        if unit == "KB":
            size *= 1024
        elif unit == "MB":
            size *= 1024 ** 2
        elif unit == "GB":
            size *= 1024 ** 3
        elif unit == "B":
            pass
        return size


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-V",
        "--version",
        version=distribution.version,
        action=_ShowVersionAction,
        help="display version",
    )
    parser.add_argument(
        "url_or_id", help="url or file/folder id (with --id) to download from"
    )
    parser.add_argument("-O", "--output", help="output file name / path")
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="suppress standard output"
    )
    parser.add_argument(
        "--id",
        action="store_true",
        help="flag to specify file/folder id instead of url",
    )
    parser.add_argument(
        "--proxy",
        help="<protocol://host:port> download using the specified proxy",
    )
    parser.add_argument(
        "--speed",
        type=file_size,
        help="download speed limit in second (e.g., '10MB' -> 10MB/s)",
    )
    parser.add_argument(
        "--no-cookies",
        action="store_true",
        help="don't use cookies in ~/.cache/gdownplus/cookies.json",
    )
    parser.add_argument(
        "--folder",
        action="store_true",
        help="download entire folder instead of a single file",
    )

    args = parser.parse_args()

    if args.output == "-":
        if six.PY3:
            args.output = sys.stdout.buffer
        else:
            args.output = sys.stdout

    if args.id and not args.folder:
        url = "https://drive.google.com/uc?id={id}".format(id=args.url_or_id)
    elif args.id and args.folder:
        url = "https://drive.google.com/folders/{id}".format(id=args.url_or_id)
    else:
        url = args.url_or_id

    if args.folder:
        download_folder(
            url,
            output=args.output,
            quiet=args.quiet,
            proxy=args.proxy,
            speed=args.speed,
            use_cookies=not args.no_cookies,
        )
    else:
        download(
            url=url,
            output=args.output,
            quiet=args.quiet,
            proxy=args.proxy,
            speed=args.speed,
            use_cookies=not args.no_cookies,
        )


if __name__ == "__main__":
    main()
