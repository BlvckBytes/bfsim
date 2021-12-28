import sys
import os
import time

from inp_handler import InpHandler

"""
Read the instructions contained in a file
at the provided path into a list of characters
"""
def read_instrs(path):
  # Target characters for execution
  tarchars = [">", "<", "+", "-", ".", ",", "[", "]"]

  # Filter out all target characters into a list of instructions
  instrs = []
  with open(path, "r") as f:
    for line in f.readlines():
      instrs.extend(filter(lambda x: x in tarchars, [c for c in line]))

  return instrs

"""
Generate a map of indices translating opening
to closing parantheses and vice versa
"""
def gen_parenmap(instrs):
  parenmap = {}
  pstack = []

  # Loop instructions indexed
  for i, instr in enumerate(instrs):
    # Opening paren, push i to stack
    if instr == '[':
      pstack.append(i)

    # Closing paren, get i from stack
    elif instr == ']':
      # Nothing remaining on the stack
      if len(pstack) == 0:
        print("Error, unbalanced parentheses encountered!")
        sys.exit()

      oi = pstack.pop()

      # Create partner entries
      parenmap[i] = oi
      parenmap[oi] = i

  # Some parens remained on the stack
  if len(pstack) > 0:
    print("Error, unbalanced parentheses encountered!")
    sys.exit()

  return parenmap

"""
Simulate a list of instruction characters

> increment pointer
< decrement pointer
+ increment cell
- decrement cell
. current cell ASCII -> stdout
, stdin ASCII -> current cell
[ jump after ] if cell == 0
] jump after [ if cell != 0
"""
def sim_instrs(instrs):
  # Start of with a single cell on the tape
  tape = [0]
  cell_ptr = 0
  instr_ptr = 0

  # Generate map of matching parantheses
  parenmap = gen_parenmap(instrs)

  # Watch user input
  inp = InpHandler()

  # Inform
  print("Whenever a new line starting with '> ' appears, a char is prompted.")
  print("After typing the char, send by hitting CTRL-D (flusing)!", end="\n\n")
  
  # Ignore newline chars
  inp.start(True)

  # Loop until end of program
  while instr_ptr != len(instrs):
    instr = instrs[instr_ptr]

    # Increase cell pointer
    if instr == ">":
      cell_ptr += 1

      # Init new cells on demand
      if len(tape) == cell_ptr:
        tape.append(0)

    # Decrease cell pointer
    elif instr == "<":
      cell_ptr -= 1

    # Increase cell value
    elif instr == "+":
      tape[cell_ptr] += 1

      # Wrap around to 0
      if tape[cell_ptr] > 255:
        tape[cell_ptr] = 0

    # Decrease cell value
    elif instr == "-":
      tape[cell_ptr] -= 1

      # Wrap around to 255
      if tape[cell_ptr] < 0:
        tape[cell_ptr] = 255

    # Write cell's ASCII value to stdout
    elif instr == ".":
      sys.stdout.write(chr(tape[cell_ptr]))
      sys.stdout.flush()

    # Read ASCII value from stdin into cell
    elif instr == ",":
      sys.stdout.write('> ')
      sys.stdout.flush()
      tape[cell_ptr] = ord(inp.getch())
    
    # Enter a loop
    elif instr == "[":
      # Jump to closing paren on zero
      if tape[cell_ptr] == 0:
        instr_ptr = parenmap[instr_ptr]
    
    # Exit a loop
    elif instr == "]":
      # Jump to opening paren on non-zero
      if tape[cell_ptr] != 0:
        instr_ptr = parenmap[instr_ptr]

    # Go to next instruction
    instr_ptr += 1

  # Stop scanning for input
  inp.stop()

"""
Main entry point of this program
"""
def main():
  # Ensure path arg
  if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <path>")
    sys.exit()

  # Create absolute path from relative if applicable
  path = sys.argv[1]
  path = path if path.startswith("/") else os.path.join(os.getcwd(), path)

  # Ensure file existence
  if not os.path.exists(path):
    print(f"The file {path} could not be located!")
    sys.exit()

  # Read the file's instructions
  instrs = read_instrs(path)

  # No valid instructions in that file
  if len(instrs) == 0:
    print(f"The file {path} contains no valid instructions!")
    sys.exit()

  # Simulate the file's program and time it
  print("--------------------< BFSIM >--------------------")
  start = time.time_ns()
  sim_instrs(instrs)
  dur = (time.time_ns() - start) / 10**6
  print(f"\nDone simulating program, took {dur}ms!")
  print("--------------------< BFSIM >--------------------")

if __name__ == "__main__":
  main()