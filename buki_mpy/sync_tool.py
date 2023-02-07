import pathlib
from buki_mpy import files
from buki_mpy import hash_tool


def get_board_hash(board_files: files.Files) -> dict[str:str]:
    hash_tool_path = hash_tool.__file__
    out = (
        board_files.run(hash_tool_path, wait_output=True, stream_output=False)
        .decode(encoding="utf-8")
        .rstrip()
        .split("\r\n")
    )
    board_hash = {}
    for i in sorted(out):
        path, digest = i.split(",")
        board_hash[path] = digest
    return board_hash


def get_local_hash(path: str):
    plib = pathlib.Path(path)
    if plib.is_absolute():
        path = str(plib.relative_to(plib.cwd()))
    else:
        path = str(plib)
    digest = hash_tool.FileHash(path)
    local_hash = {}
    for p, d in sorted(digest.hashes, key=lambda x: x[0]):
        p = p.lstrip(path)
        local_hash[p] = d
    return local_hash


def compare(pri: dict, sec: dict):  # subをmainに揃える
    pri_set = set(pri.keys())
    sec_set = set(sec.keys())
    name_set: set[str] = pri_set | sec_set
    new_files = []
    remove_files = []
    overwrite_files = []
    for i in name_set:
        if i in pri_set and i in sec_set:
            if i.endswith("/"):
                continue
            if pri[i] != sec[i]:
                overwrite_files.append(i)
        elif i in pri_set and i not in sec_set:
            new_files.append(i)
        else:
            remove_files.append(i)
    return new_files, overwrite_files, remove_files
