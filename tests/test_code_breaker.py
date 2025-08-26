import pytest
from mastermind import CodeBreaker
from mastermind import CodeEntry

@pytest.mark.parametrize("user_input, expected", [
  ("1234", "1234"),
  ("333", "333"),     #note: even though CodeEntry is "invalid", CodeBreaker does not make the check
  ("asg", "asg"),
  ("", "")
])
def test_make_guess(monkeypatch, user_input, expected):
  """Automated input for CodeEntry object return."""
  code_breaker = CodeBreaker(4,8)

  monkeypatch.setattr("builtins.input", lambda _: user_input)
  guess_code = code_breaker.make_guess()
  assert isinstance(guess_code, CodeEntry)
  assert guess_code.sequence == expected