import pytest
from mastermind import CodeEntry
from mastermind import Feedback

@pytest.mark.parametrize("sequence, code_length, code_range", [
  ("1234", 4, 8),
  ("0000", 4, 8),
  ("0011", 4, 8),
])
def test_valid_code(sequence, code_length, code_range):
  assert CodeEntry(sequence, code_length, code_range).is_valid()  #valid case
  assert CodeEntry(sequence, code_length, code_range).is_valid()  #valid case, test for 0
  assert CodeEntry(sequence, code_length, code_range).is_valid()  #valid case, test for duplicates

@pytest.mark.parametrize("sequence, code_length, code_range", [
  ("1232445", 4, 8),  #too long
  ("123", 4, 8),      #too short 
  ("", 4, 8)          #too short (blank)
])
def test_invalid_code_length(sequence, code_length, code_range):
  """CodeEntry should be invalid if length is incorrect."""
  assert not CodeEntry(sequence, code_length, code_range).is_valid()

@pytest.mark.parametrize("sequence, code_length, code_range", [
  ("1.23", 4, 8),     #. is not a digit
  ("!2a3", 4, 8),     #!a are not digits
  ("f@$z", 4, 8),     #f@$z are not digits
  ("1 34", 4, 8),     #whitespace is not a digit
  ("    ", 4, 8)      #whitespaces are not a digit
])
def test_invalid_code_nondigit(sequence, code_length, code_range):
  """CodeEntry should be invalid if code contains non-digit."""
  assert not CodeEntry(sequence, code_length, code_range).is_valid()

@pytest.mark.parametrize("sequence, code_length, code_range", [
  ("1239" , 4, 8),    #9 is outside of range
  ("8989", 4, 8)      #8 and 9 are outside of range
])
def test_invalid_code_range(sequence, code_length, code_range):
  """CodeEntry should be invalid if any value is greater than range."""
  assert not CodeEntry(sequence, code_length, code_range).is_valid()

def test_string():
  """to_string() return expected to be the same as its sequence."""
  code = CodeEntry("1234", 4, 8)
  assert code.to_string() == "1234"

def test_compare_codes_feedback_return():
  """Comparison between two CodeEntry should return Feedback object."""
  code1 = CodeEntry("1234", 4, 8)
  code2 = CodeEntry("1234", 4, 8)
  feedback = code1.compare_with(code2)
  assert isinstance(feedback, Feedback)

@pytest.mark.parametrize("seq1, seq2, length, range, loc_count, num_count, loc_count_same", [
  ("1234", "1234", 4, 8, 4, 4, True),     #all correct loc/num
  ("1234", "1577", 4, 8, 1, 1, True),     #one correct loc/num
  ("1234", "1537", 4, 8, 2, 2, True),     #some correct loc/num
  ("1234", "7777", 4, 8, 0, 0, True),     #no correct loc/num
  ("1234", "1341", 4, 8, 1, 3, False),    #one correct loc, some correct num
  ("1122", "2211", 4, 8, 0, 4, False),    #no correct loc, all correct num
])
def test_compare_codes(seq1, seq2, length, range, loc_count, num_count, loc_count_same):
  """Comparison feedback result tests."""
  code1 = CodeEntry(seq1, length, range)
  code2 = CodeEntry(seq2, length, range)
  feedback = code1.compare_with(code2)
  assert (feedback.correct_location == feedback.correct_number)== loc_count_same
  assert feedback.correct_location == loc_count
  assert feedback.correct_number == num_count