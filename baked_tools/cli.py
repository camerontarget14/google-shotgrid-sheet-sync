import sys
import argparse
import logging

from . import MAINTAINER, __version__, uploader
from .sheet_sync import sync
from .lib.logging import configure_logging


logger = logging.getLogger(__name__)


def print_version():
    print(__version__)


def run_upload(args):
    success = uploader.upload_movies(
        args.project_name, args.movie_filepaths, args.dry_run,
    )
    sys.exit(0 if success else 1)


def run_sync(args):
    success = sync(args.project_name)
    sys.exit(0 if success else 1)


def run():
    parser = argparse.ArgumentParser(
        description=f"""
Baked command-line tool for Shotgrid. For more help, contact {MAINTAINER}.
    """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        default="WARN",
        help="Set log level",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print version and exit",
    )
    parser.set_defaults(func=lambda _: parser.print_usage())
    subparsers = parser.add_subparsers(title="Subcommands")

    # =========================================================================
    # Upload
    # =========================================================================
    upload_subparser = subparsers.add_parser(
        "upload", help="Upload media to Shotgrid"
    )
    upload_subparser.add_argument(
        "project_name",
        type=str,
        help="Project name.",
    )
    upload_subparser.add_argument(
        "movie_filepaths",
        type=str,
        nargs="+",
        metavar="movie_filepath",
        help="Path to a movie file to upload.",
    )
    upload_subparser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Use this option to test the tool without actually uploading anything.",
    )
    upload_subparser.set_defaults(func=run_upload)

    # =========================================================================
    # Google Sheet Shot Status Sync
    # =========================================================================
    sync_subparser = subparsers.add_parser(
        "sync", help="Sync shots data with Google sheet"
    )
    sync_subparser.add_argument(
        "project_name",
        type=str,
        help="Project name.",
    )
    sync_subparser.set_defaults(func=run_sync)

    # =========================================================================

    args = parser.parse_args()
    configure_logging(args.loglevel)
    logger.info(f"Python version: {sys.version}")

    if args.version:
        print_version()
    else:
        args.func(args)
