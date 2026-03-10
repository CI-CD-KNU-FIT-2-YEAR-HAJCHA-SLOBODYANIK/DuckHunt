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

def test_score_update_time_not_expired(score_instance):
    """Перевірка, що час не вичерпано при dt=1.0"""
    is_expired = score_instance.update_time(1.0)
    assert is_expired is False

def test_score_update_time_expired(score_instance):
    """Перевірка, що повертає True, коли час виходить"""
    is_expired = score_instance.update_time(60.1)
    assert is_expired is True