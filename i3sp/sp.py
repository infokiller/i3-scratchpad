import logging
from typing import List

import i3ipc

# NOTE: this prefix is used by i3-track-last so it must not be changed without
# updating that script.
_SCRATCHPAD_MARK_PREFIX = '_sp'

_LIST_CONTAINERS_HEADER = [
    'id', 'in_scratchpad_workspace', 'window_class', 'window_instance'
]

logger = logging.getLogger()


def is_scratchpad_mark(mark: str) -> bool:
    return mark.startswith(_SCRATCHPAD_MARK_PREFIX)


def is_scratchpad_container(container: i3ipc.Con) -> bool:
    return any(is_scratchpad_mark(m) for m in container.marks)


def get_scratchpad_containers(root: i3ipc.Con) -> List[i3ipc.Con]:
    return [c for c in root if is_scratchpad_container(c)]


def is_floating(container):
    if container.type == 'floating_con':
        return True
    if not container.parent:
        return False
    return container.parent.type == 'floating_con'


def _add_mark(container: i3ipc.Con, mark: str):
    container.command('mark --add "{}"'.format(mark))


def _set_marks(container: i3ipc.Con, marks: List[str]):
    container.marks = marks
    if not marks:
        return
    container.command('mark "{}"'.format(marks[0]))
    for mark in marks[1:]:
        _add_mark(container, mark)


def mark_as_scratchpad(container: i3ipc.Con) -> None:
    if is_scratchpad_container(container):
        logger.info(
            'Container already marked for scratchpad, not marking it again.')
        return
    name = container.window_instance
    mark = '{}:{}:{}'.format(_SCRATCHPAD_MARK_PREFIX, name, container.id)
    _add_mark(container, mark)


def print_scratchpad_containers(tree: i3ipc.Con) -> None:
    scratchpad_workspace_id = tree.scratchpad().id
    table = [_LIST_CONTAINERS_HEADER]
    for con in get_scratchpad_containers(tree):
        # pylint: disable-next=superfluous-parens
        in_scratchpad = (con.workspace().id == scratchpad_workspace_id)
        table.append(
            [con.id, in_scratchpad, con.window_class, con.window_instance])
    print('\n'.join('\t'.join(str(e) for e in row) for row in table))


def scratch_or_kill(container):
    if is_scratchpad_container(container):
        container.command('move scratchpad')
    else:
        container.command('kill')


def move_to_scratchpad(container):
    container.command('move scratchpad')


def toggle_last_container(tree, process_workspace_containers, dock):
    focused = tree.find_focused()
    if is_scratchpad_container(focused) and is_floating(focused):
        move_to_scratchpad(focused)
        return
    focused_workspace = focused.workspace()
    if process_workspace_containers:
        # sp_containers = get_scratchpad_containers(focused_workspace)
        # if sp_containers:
        #     move_to_scratchpad(sp_containers[0])
        #     return
        for container in get_scratchpad_containers(focused_workspace):
            if is_floating(container):
                move_to_scratchpad(container)
                return
    containers = tree.scratchpad().leaves()
    if not containers:
        return
    if dock:
        focused_workspace.command('split horizontal')
        containers[-1].command(
            'move workspace current, focus, floating disable, '
            'resize set 50 ppt, move left, move left, move left')
    else:
        containers[-1].command('move workspace current, focus')
