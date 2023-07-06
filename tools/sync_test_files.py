"""Synchronizes test files that require the future annotation import.

.. versionadded:: 2.0
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Iterable

from ilikesql.util.tool_support import code_writer_cmd

header = '''\
"""This file is automatically generated from the file
{source!r}
by the {this_file!r} script.

Do not edit manually, any change will be lost.
"""  # noqa: E501

from __future__ import annotations

'''

home = Path(__file__).parent.parent
this_file = Path(__file__).relative_to(home).as_posix()
remove_str = "# anno only: "


def run_operation(
    name: str, source: str, dest: str, cmd: code_writer_cmd
) -> None:
    source_data = Path(source).read_text().replace(remove_str, "")
    dest_data = header.format(source=source, this_file=this_file) + source_data

    cmd.write_output_file_from_text(dest_data, dest)


def main(file: str, cmd: code_writer_cmd) -> None:
    if file == "all":
        operations: Iterable[Any] = files.items()
    else:
        operations = [(file, files[file])]

    for name, info in operations:
        run_operation(name, info["source"], info["dest"], cmd)


files = {
    "typed_annotation": {
        "source": "test/orm/declarative/test_typed_mapping.py",
        "dest": "test/orm/declarative/test_tm_future_annotations_sync.py",
    }
}

if __name__ == "__main__":
    cmd = code_writer_cmd(__file__)
    with cmd.add_arguments() as parser:
        parser.add_argument(
            "--file", choices=list(files) + ["all"], default="all"
        )

    with cmd.run_program():
        main(cmd.args.file, cmd)
