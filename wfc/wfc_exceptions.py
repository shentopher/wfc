# Exceptions
class Contradiction(Exception):
    """Solving could not proceed without backtracking/restarting."""
    pass


class TimedOut(Exception):
    """Solve timed out."""
    pass


class StopEarly(Exception):
    """Aborting solve early."""
    pass
