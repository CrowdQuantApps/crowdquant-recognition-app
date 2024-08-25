import sys


def print_error(*args, sep=' ', end='\n', file=None):  # known special case of print
    """
    Prints the values to a stream, or to sys.Stdout by default.

      sep
        string inserted between values, default a space.
      end
        string appended after the last value, default a newline.
      file
        a file-like object (stream); defaults to the current sys.stdout.
      flush
        whether to forcibly flush the stream.
    """
    if file is None:
        file = sys.stderr

    message = sep.join(str(arg) for arg in args) + end
    colored_message = f"\033[38;2;{223};{0};{0}m{message}\033[0m"  # Set color to Red

    file.write(colored_message)
