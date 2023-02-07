from buki_mpy import files
from buki_mpy import hash_tool


def get_board_hash(board_files: files.Files) -> list[tuple[str, bytes]]:
    hash_tool_path = hash_tool.__file__
    return board_files.run(hash_tool_path, wait_output=True, stream_output=False)
