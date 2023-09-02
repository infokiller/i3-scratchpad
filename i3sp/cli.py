#!/usr/bin/env python3
# pylint: disable=invalid-name

import argparse
import logging

import i3ipc

from i3sp import sp


def _init_logger(logger) -> None:
    stdout_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)


def _create_args_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Manage scratchpad containers.')
    parser.add_argument(
        '--log-level',
        choices=('debug', 'info', 'warning', 'error', 'critical'),
        default='warning',
        help='Logging level for stderr.')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    subparsers.add_parser(
        'list-containers', help='List all scratchpad workspaces.')
    subparsers.add_parser(
        'scratch-or-kill',
        help='If the focused container is a scratchpad container, move it back '
        'to the scratchpad. Otherwise, kill it.')
    subparsers.add_parser(
        'move', help='Moves the focused container to the scratchpad.')
    toggle_parser = subparsers.add_parser(
        'toggle-last',
        help='Shows the last scratchpad container. Note that this is not the '
        'same as i3\'s builtin "scratchpad show" command, which will show you '
        'the first scratchpad container.')
    toggle_parser.add_argument(
        '--process-workspace-containers',
        dest='process_workspace_containers',
        action='store_true',
        help='When processing of workspace containers is on, will also '
        'consider scratchpad containers in the focused workspace if they are '
        'unfocused, before looking up a container from the scratchpad.')
    toggle_parser.add_argument(
        '--no-process-workspace-containers',
        dest='process_workspace_containers',
        action='store_false')
    toggle_parser.set_defaults(process_workspace_containers=True)
    toggle_parser.add_argument(
        '--dock',
        dest='dock',
        action='store_true')
    toggle_parser.add_argument(
        '--no-dock',
        dest='dock',
        action='store_false')
    toggle_parser.set_defaults(dock=False)
    return parser


def main():
    logger = sp.logger
    _init_logger(logger)
    args = _create_args_parser().parse_args()
    logger.setLevel(getattr(logging, args.log_level.upper(), None))
    i3_connection = i3ipc.Connection()
    tree = i3_connection.get_tree()
    if args.command == 'list-containers':
        sp.print_scratchpad_containers(tree)
    if args.command == 'scratch-or-kill':
        sp.scratch_or_kill(tree.find_focused())
    elif args.command == 'move':
        focused = tree.find_focused()
        sp.mark_as_scratchpad(focused)
        sp.move_to_scratchpad(focused)
    elif args.command == 'toggle-last':
        sp.toggle_last_container(
            tree, args.process_workspace_containers, args.dock)


if __name__ == '__main__':
    main()
