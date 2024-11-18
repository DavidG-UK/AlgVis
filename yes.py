import sys

# Global variable to store the current line
current_line = None

def trace_lines(frame, event, arg):
    global current_line
    if event == 'line':
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        with open(filename) as f:
            current_line = f.readlines()[lineno - 1].strip()
            print(f"Executing line {lineno}: {current_line}")
    return trace_lines

sys.settrace(trace_lines)

# Example code
def example_function():
    a = 1
    b = 2
    c = a + b
    print(c)

example_function()

# You can use the `current_line` variable here if needed
print(f"Last executed line: {current_line}")

