import hashlib
import os
import binascii

S_IFMT = 0xF000  # MASK
S_IFREG = 0x8000  # Regular file
S_IfDIR = 0x4000  # directory


def main():
    f = FileHash("/")
    for path, digest in f.hashes:
        print(path, digest, sep=",")


class FileHash:
    def __init__(self, start_path, func_name="sha1") -> None:
        if func_name == "md5":
            self.hash_func = hashlib.md5
        elif func_name == "sha1":
            self.hash_func = hashlib.sha1
        elif func_name == "sha256":
            self.hash_func = hashlib.sha256
        self.hashes = []

        self.solve_hash(start_path)

    def isdir(self, path) -> bool:
        file_mode = os.stat(path)[0] & S_IFMT
        return file_mode == S_IfDIR

    def solve_hash(self, path: str):
        hash_func = self.hash_func()
        if self.isdir(path):  # if directory it is recallsive
            if not path.endswith("/"):
                path += "/"
            file_list = sorted(os.listdir(path))
            for i in file_list:
                child = path + i
                hash_func.update(self.solve_hash(child))
        else:
            with open(path, mode="rb") as f:
                hash_func.update(f.read())
        hash_digest = hash_func.digest()
        self.hashes.append((path, str(binascii.hexlify(hash_digest), "ascii")))
        return hash_digest


if __name__ == "__main__":
    main()
