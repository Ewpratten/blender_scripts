import abc


class PreflightCheckResult:
    """Returnable metadata about a past check"""

    success: bool

    def __init__(self, success: bool):
        self.success = success


class PreflightCheck(metaclass=abc.ABCMeta):
    """A common base class for preflight checks"""

    def __init__(self, has_autofix_capability: bool):
        super().__init__()
        self._has_autofix_capability = has_autofix_capability

    @abc.abstractmethod
    def run_check(self) -> PreflightCheckResult:
        """Runs the check and returns the result"""
        raise NotImplementedError

    @abc.abstractmethod
    def run_fix(self, result: PreflightCheckResult) :
        """Tries to auto-fix the check"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self) -> str:
        """Returns the name of the check"""
        raise NotImplementedError
    
    def can_auto_fix(self) -> bool:
        """Returns whether the check can be auto-fixed"""
        return self._has_autofix_capability
