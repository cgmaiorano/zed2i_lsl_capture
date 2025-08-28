import argparse
from typing import List, Optional

from core import without_stimulus_orchestrator


def parse_arguments(args: Optional[List[str]]) -> argparse.Namespace:
    """Argument parser for zed2i_3d_lsl_capture cli.

    Args:
        args: A list of command line arguments given as strings. If None, the parser
            will take the args from `sys.argv`.

    Returns:
        Namespace object with all the input arguments and default values.

    Raises:
        SystemExit: if arguments are None.
    """
    parser = argparse.ArgumentParser(
        description="Collect ZED motion tracking data with or without a stimulus and stream to LSL.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Please report issues at https://github.com/childmindresearch/zed2i_3d_lsl_capture.",
    )
    parser.add_argument(
        "-p",
        "--participant",
        type=str,
        required=True,
        help="Participant ID.",
    )

    parser.add_argument(
        "-s",
        "--sequence",
        type=str,
        required=True,
        help="Integer value representing current sequence or trial number.",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None):
    arguments = parse_arguments(args)
    without_stimulus_orchestrator.run(arguments.participant, arguments.sequence)
