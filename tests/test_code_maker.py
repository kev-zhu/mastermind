import pytest
from mastermind import CodeMaker
from mastermind import CodeEntry
from mastermind import Feedback

# @pytest.mark.parametrize("code_length, code_range", [
#   (4, 8),   #standard game request
#   (0, 8)    #force an error on API call with length = 0, will use in-house generator
# ])
# def test_generate_code(code_length, code_range):
#   """API call or in-house generator should update CodeMaker's secret code."""
#   code_maker = CodeMaker(code_length, code_range)
#   code_maker.generate_code()
#   assert code_maker.secret_code != None
#   assert len(code_maker.secret_code.sequence) == code_length

@pytest.mark.parametrize("code_length, code_range", [
  (4, 8),   #generate 4 numbers from 0-7
  (1, 8),   #generate 1 number from 0-7
  (0, 5),   #generated 0 numbers from 0-4
  (0, 0)    #generated 0 numbers from 0 (should be empty string)
])
def test_in_house_random_seq_gen(code_length, code_range):
  """Should generate a sequence of number in string format of CodeMaker's specified length and range."""
  code_maker = CodeMaker(code_length, code_range)
  sequence = code_maker.use_in_house_random_seq_gen()
  assert all([0 <= int(c) < code_range for c in sequence])  #test for range
  assert len(sequence) == code_length                       #test for length

def test_get_hint_pos_dict():
  """Should have a formatted dict that both position and value of secret."""
  code_maker = CodeMaker(4, 8)
  code_maker.generate_code()
  hint_dict = code_maker.get_hint_position_dict()
  rebuilt_secret = ["x"] * 4
  for key in hint_dict.keys():
    rebuilt_secret[key] = hint_dict[key]
  assert isinstance(hint_dict, dict)
  assert len(hint_dict) == len(code_maker.secret_code.sequence)
  assert code_maker.secret_code.sequence == "".join(rebuilt_secret)

def test_evaluate_code():
  """Method calls on Code comparison: should return Feedback object"""
  code_maker = CodeMaker(4, 8)                        #ensure perfect feedback object is returned across calls
  code_maker.secret_code = CodeEntry("1234", 4, 8)
  sample_code = CodeEntry("1234", 4, 8)
  feedback = code_maker.evaluate_code(sample_code)
  assert isinstance(feedback, Feedback)
  assert feedback.is_perfect_response()