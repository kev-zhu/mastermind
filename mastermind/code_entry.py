from collections import Counter
from .feedback import Feedback

class CodeEntry:
  """Handles ONLY CodeEntry logic."""
  def __init__(self, sequence: str, length_rule: int, range_rule: int):
    self.sequence = sequence
    self.length_rule = length_rule
    self.range_rule = range_rule
  
  def compare_with(self, other_code: "CodeEntry") -> Feedback:
    """
    Compare this code with another CodeEntry object.

    Args:
      other_code(CodeEntry): The other code being compared to.
   
    Returns:
      Feedback: Organized result of comparison.
    """
    def count_num() -> int:
      """Returns count of shared numbers between two code sequences."""
      count = 0
      this_dict = Counter(self.sequence)
      other_dict = Counter(other_code.sequence)
      
      for key in other_dict.keys():
        if this_dict[key]:
          count += min(this_dict[key], other_dict[key])
      return count

    def count_loc() -> int:
      """Returns count of indexes that shares the same value between two code sequences."""
      count = 0
      for i in range(len(self.sequence)):
        if(self.sequence[i] == other_code.sequence[i]):
          count += 1
      return count

    correct_num_count = count_num()
    correct_loc_count = count_loc()

    return Feedback(correct_num_count, correct_loc_count, self.length_rule)

  def is_valid(self) -> bool:
    """
    Checks if Code sequence follows digits, length, and range rules.
    
    Returns:
      bool: True if is valid, False otherwise.
    """
    # length validity
    if len(self.sequence) != self.length_rule:
      return False
    # digits validity
    elif not self.sequence.isdigit():
      return False
    # range validiity
    elif not all(map(lambda x: 0 <= int(x) < self.range_rule, self.sequence)):    
      return False
    else:
      return True

  def to_string(self) -> str:
    """Return Code sequence."""
    return self.sequence
