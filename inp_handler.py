import threading
import select
import sys

class InpHandler:

  source = []

  """
  Get a string of characters until the specified
  terminator ocurrs
  """
  def getstr(self, until):
    chars = []

    # Read chars into array until terminator is met
    char = self.getch()
    while char != until:
      chars.append(char)
      char = self.getch()

    return chars

  """
  Get the next character available from input source
  """
  def getch(self, wipe=False):
    # Wait until a character is available
    while len(self.source) == 0:
      continue

    # Return first received character
    ch = self.source.pop(0)

    # Clear source if flag is set
    if wipe:
      self.source = []
    
    return ch

  """
  Start watching the input source for new data
  """
  def scan(self, rm_nl):
    # Scan as long as scanning is active
    while self.is_scanning:

      # Wait until data is available
      while not select.select([sys.stdin, ], [], [], 0.0)[0] and self.is_scanning:
        continue
        
      # Scanning quitted in the mean time
      if not self.is_scanning:
        break

      # Read individual chars
      chars = [c for c in sys.stdin.read()]

      # Remove newline if flag is set
      if rm_nl:
        chars = filter(lambda x: x != '\n', chars)

      self.source.extend(chars)

  """
  Watch for data in another thread
  """
  def start(self, rm_nl=False):
    self.t = threading.Thread(target=self.scan, args=(rm_nl,))
    self.is_scanning = True
    self.t.start()

  """
  Stop watching
  """
  def stop(self):
    self.is_scanning = False