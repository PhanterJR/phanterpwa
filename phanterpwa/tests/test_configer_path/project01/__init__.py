import os
import glob

current_path = os.path.dirname(__file__)
__all__ = [os.path.basename(x) for x in glob.glob(os.path.join(current_path, "*"))
    if os.path.isdir(x) and not os.path.basename(x).startswith("_")]
if __name__ == '__main__':
    print(__all__)
