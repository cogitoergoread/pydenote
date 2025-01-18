import os


class DeNote:
    def chk_dir(self, dir: str, environstr: str) -> bool:
        home_dir = dir if dir else os.environ.get(environstr, ".")
        if not os.path.exists(home_dir) or not os.access(home_dir, os.W_OK):
            print(f"Folder {home_dir} is not ready for writing files.")
            return False
        self.path = home_dir
        return True
