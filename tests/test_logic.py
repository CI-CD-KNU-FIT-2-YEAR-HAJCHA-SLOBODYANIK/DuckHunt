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

def test_score_increment_hit(score_instance):
    """Перевірка +100 очок та +1 хіт"""
    initial_points = score_instance.points
    score_instance.increment_hit()
    
    assert score_instance.points == initial_points + 100
    assert score_instance.hits == 1