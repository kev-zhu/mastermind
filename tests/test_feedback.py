import pytest
from mastermind import Feedback

@pytest.mark.parametrize("correct_num, correct_loc, code_length, perfect", [
  (4, 4, 4, True),    #True - perfect case
  (2, 2, 4, False),   #False - imperfect case
  (1, 1, 4, False),   #False - imperfect case
  (2, 1, 4, False),   #False - imperfect case
  (0, 0, 4, False)    #False - imperfect case
])
def test_feedback_is_perfect_response(correct_num, correct_loc, code_length, perfect):
  """Feedback should be perfect when correct_num = correct_loc = code_length."""
  feedback = Feedback(correct_num, correct_loc, code_length)
  assert feedback.is_perfect_response() == perfect

@pytest.mark.parametrize("correct_num, correct_loc, code_length, feedback_string", [
  (4, 4, 4, "4 correct numbers and 4 correct locations"),   #4nums/4locs
  (2, 2, 4, "2 correct numbers and 2 correct locations"),   #2nums/2locs
  (1, 1, 4, "1 correct number and 1 correct location"),     #1num/1loc
  (2, 1, 4, "2 correct numbers and 1 correct location"),    #2nums/1loc
  (0, 0, 4, "0 correct numbers and 0 correct locations")    #0nums/0locs
])
def test_feedback_to_string(correct_num, correct_loc, code_length, feedback_string):
  """Feedback should be a formatted string."""
  feedback = Feedback(correct_num, correct_loc, code_length)
  assert feedback.to_string() == feedback_string