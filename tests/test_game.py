import pytest
from unittest.mock import MagicMock
from mastermind import Game
from mastermind import CodeBreaker
from mastermind import CodeMaker
from mastermind import CodeEntry
from mastermind import Feedback

#UNIT TESTS
def test_game_start():
  """Should have updated version of game state after start() runs"""
  game = Game()
  assert game.code_maker == None
  assert game.code_breaker == None
  assert game.turn == 0
  assert game.active_game == False
  game.start()
  assert isinstance(game.code_maker, CodeMaker)
  assert isinstance(game.code_breaker, CodeBreaker)
  assert game.turn == 1
  assert game.active_game

def test_code_breaker_guess_request(monkeypatch):
  """Automate input with monkeypatch to test for valid Code Breaker guess entry."""
  monkeypatch.setattr("builtins.input", lambda _:"1234")
  game = Game()
  game.code_breaker = CodeBreaker(4, 8)
  guess_code = game.request_code_breaker_guess()
  assert isinstance(guess_code, CodeEntry)
  assert guess_code.is_valid()

@pytest.mark.parametrize("sample_code_sequence, perfect, sample_feedback_string", [
  ("1234", True, "4 correct numbers and 4 correct locations"),
  ("1243", False, "4 correct numbers and 2 correct locations"),
  ("0567", False, "0 correct numbers and 0 correct locations")
])
def test_request_code_maker_perfect_evaluation(sample_code_sequence, perfect, sample_feedback_string):
  """Should print string formatted Feedback and return Feedback object."""
  game = Game()
  game.code_maker = CodeMaker(4, 4)
  game.code_maker.secret_code = CodeEntry("1234", 4, 8)
  sample_guess_code = CodeEntry(sample_code_sequence, 4, 8)
  sample_feedback = game.request_code_maker_evalulation(sample_guess_code)
  assert isinstance(sample_feedback, Feedback)
  assert sample_feedback.is_perfect() == perfect
  assert sample_feedback.to_string() == sample_feedback_string

def test_update_game_state_history_and_turns(dummy_code = "1234", dummy_length=4, dummy_range=8):
  """Should update states of game to prepare for next game move."""
  game = Game()
  game.start()
  game.current_guess = CodeEntry(dummy_code, dummy_length, dummy_range)
  game.current_feedback = Feedback(dummy_length, dummy_length, dummy_length)
  game.update_game_state()
  assert game.history == [(game.current_guess, game.current_feedback)]
  assert game.turn == 2
  assert game.code_breaker.turn == 2

def test_game_is_over_max_attempts_reached():
  """Simulate Code Maker win with turn reaching past max_attempts"""
  game = Game(max_attempt=1)
  game.turn = 2
  assert game.is_over()
  assert not game.active_game
  assert game.winner == "Code Maker"

def test_game_is_over_perfect_guess_feedback():
  """Simulate Code Breaker win with correct guess"""
  game = Game()
  perfect_feedback = Feedback(4, 4, 4)
  game.current_feedback = perfect_feedback
  assert game.is_over()
  assert not game.active_game
  assert game.winner == "Code Breaker"

def test_get_correct_history_format():
  """History retrieval of previous game moves."""
  game = Game()
  game.code_breaker = CodeBreaker(4, 4)
  game.current_guess = CodeEntry("1234", 4, 8)
  game.current_feedback = Feedback(0, 0, 4)
  game.update_game_state()
  history_str = game.get_history()
  assert f"Guess #1: 1234 - {game.current_feedback.to_string()}" in history_str
  assert f"Guess #2:" not in history_str

  game.current_guess = CodeEntry("2345", 4, 8)
  game.current_feedback = Feedback(1, 1, 4)
  game.update_game_state()
  history_str = game.get_history()
  assert f"Guess #1: 1234 -" in history_str
  assert f"Guess #2: 2345 - {game.current_feedback.to_string()}" in history_str

#COMPONENT TESTS w/ monkeypatch and MagicMock
def test_game_end_to_end_breaker_wins(monkeypatch):
  """Simulates middle of game where Code Maker returns a perfect Feedback response and ends game after."""
  game = Game(max_attempt=3)
  game.start()

  #simulate a move in the middle of a game where the code breaker's guess has a perfect feedback response
  game.code_maker = MagicMock()
  monkeypatch.setattr("builtins.input", lambda _:"1234")
  mock_feedback = MagicMock()
  mock_feedback.is_perfect.return_value = True
  game.current_feedback = mock_feedback
  game.code_maker.evaluate_code.return_value = mock_feedback
  game.make_move()
  #game.run() called here to do a check for the next game move following game move
  game.run()
  assert game.winner == "Code Breaker"
  assert not game.active_game

def test_game_end_to_end_maker_wins():
  """Simulate last guess attempt of game where Code Breaker makes an incorrect guess."""
  game = Game(max_attempt=3)
  game.start()
  game.turn = game.max_attempt    #move onto last move

  #simulate last attempt move where guess is not perfect
  game.code_breaker = MagicMock()
  game.code_maker = MagicMock()
  mock_guess = MagicMock()
  mock_guess.is_valid.return_value = True
  game.code_breaker.make_guess_return_value = mock_guess
  mock_feedback = MagicMock()
  mock_feedback.is_perfect.return_value = False
  game.code_maker.evalulate_code.return_value = mock_feedback
  game.make_move()
  #game.run() called here to do a check for the next game move following game move
  game.run()
  assert game.winner == "Code Maker"
  assert not game.active_game
  assert game.turn == game.max_attempt + 1