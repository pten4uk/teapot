import os
import sys
from pathlib import Path

import pytest

sys.path.append(os.path.join(Path(__file__).resolve().parent, 'src'))


if __name__ == '__main__':
    pytest.main(['-s', '-v'])

