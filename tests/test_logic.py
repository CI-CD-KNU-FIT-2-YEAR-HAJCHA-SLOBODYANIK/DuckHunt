import pytest
from unittest.mock import MagicMock, patch

with patch('pygame.display.set_mode'), \
     patch('pygame.font.SysFont'), \
     patch('pygame.init'):
    from engine import Game, Score, Difficulty

@pytest.fixture
def score_instance():
    """Створює чистий об'єкт рахунку перед кожним тестом"""
    return Score()