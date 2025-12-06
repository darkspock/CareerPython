"""
JsonLogic Evaluator Service

A custom implementation of JsonLogic for evaluating validation rules.
Supports the common operators needed for field validation in workflow stages.

JsonLogic format:
{
    "operator": [arg1, arg2, ...]
}

Supported operators:
- Comparison: ==, !=, >, <, >=, <=
- Logic: and, or, not, if
- Data access: var
- Array: in, all, some, none
- String: cat, substr
- Numeric: +, -, *, /, %, min, max
- Type: missing, missing_some

Reference: https://jsonlogic.com/
"""

from typing import Any, Callable, Dict, List, Optional, Union


class JsonLogicError(Exception):
    """Exception raised when JsonLogic evaluation fails"""
    pass


class JsonLogicEvaluator:
    """
    Evaluates JsonLogic rules against data.

    Usage:
        evaluator = JsonLogicEvaluator()
        result = evaluator.apply(rule, data)

    Example:
        rule = {">=": [{"var": "age"}, 18]}
        data = {"age": 21}
        result = evaluator.apply(rule, data)  # Returns True
    """

    def __init__(self) -> None:
        self._operators: Dict[str, Callable[[List[Any], Dict[str, Any]], Any]] = {
            # Comparison operators
            "==": self._op_equals,
            "===": self._op_strict_equals,
            "!=": self._op_not_equals,
            "!==": self._op_strict_not_equals,
            ">": self._op_greater_than,
            ">=": self._op_greater_than_or_equal,
            "<": self._op_less_than,
            "<=": self._op_less_than_or_equal,

            # Logic operators
            "and": self._op_and,
            "or": self._op_or,
            "!": self._op_not,
            "!!": self._op_double_not,
            "if": self._op_if,

            # Data access
            "var": self._op_var,

            # Array operators
            "in": self._op_in,
            "all": self._op_all,
            "some": self._op_some,
            "none": self._op_none,
            "merge": self._op_merge,

            # String operators
            "cat": self._op_cat,
            "substr": self._op_substr,

            # Numeric operators
            "+": self._op_add,
            "-": self._op_subtract,
            "*": self._op_multiply,
            "/": self._op_divide,
            "%": self._op_modulo,
            "min": self._op_min,
            "max": self._op_max,

            # Type operators
            "missing": self._op_missing,
            "missing_some": self._op_missing_some,
        }

    def apply(
            self,
            rule: Union[Dict, List, Any],
            data: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Apply a JsonLogic rule to data.

        Args:
            rule: The JsonLogic rule to evaluate
            data: The data context to evaluate against

        Returns:
            The result of evaluating the rule

        Raises:
            JsonLogicError: If the rule is invalid or evaluation fails
        """
        if data is None:
            data = {}

        # If rule is not a dict, return it as-is (literal value)
        if not isinstance(rule, dict):
            return rule

        # Empty dict returns empty dict
        if not rule:
            return rule

        # Get the operator and arguments
        operator = list(rule.keys())[0]
        args = rule[operator]

        # Ensure args is a list
        if not isinstance(args, list):
            args = [args]

        # Check if operator is supported
        if operator not in self._operators:
            raise JsonLogicError(f"Unknown operator: {operator}")

        # Execute the operator
        return self._operators[operator](args, data)

    def _resolve(self, value: Any, data: Dict[str, Any]) -> Any:
        """Recursively resolve a value, applying rules if needed"""
        if isinstance(value, dict):
            return self.apply(value, data)
        return value

    # Comparison operators
    def _op_equals(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Loose equality (==)"""
        if len(args) < 2:
            return False
        a = self._resolve(args[0], data)
        b = self._resolve(args[1], data)
        return bool(a == b)

    def _op_strict_equals(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Strict equality (===)"""
        if len(args) < 2:
            return False
        a = self._resolve(args[0], data)
        b = self._resolve(args[1], data)
        return bool(a == b and type(a) == type(b))

    def _op_not_equals(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Loose inequality (!=)"""
        return not self._op_equals(args, data)

    def _op_strict_not_equals(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Strict inequality (!==)"""
        return not self._op_strict_equals(args, data)

    def _op_greater_than(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Greater than (>)"""
        if len(args) < 2:
            return False
        a = self._resolve(args[0], data)
        b = self._resolve(args[1], data)
        try:
            return float(a) > float(b)
        except (TypeError, ValueError):
            return False

    def _op_greater_than_or_equal(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Greater than or equal (>=)"""
        if len(args) < 2:
            return False
        a = self._resolve(args[0], data)
        b = self._resolve(args[1], data)
        try:
            return float(a) >= float(b)
        except (TypeError, ValueError):
            return False

    def _op_less_than(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Less than (<)"""
        if len(args) < 2:
            return False
        a = self._resolve(args[0], data)
        b = self._resolve(args[1], data)
        try:
            return float(a) < float(b)
        except (TypeError, ValueError):
            return False

    def _op_less_than_or_equal(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Less than or equal (<=)"""
        if len(args) < 2:
            return False
        a = self._resolve(args[0], data)
        b = self._resolve(args[1], data)
        try:
            return float(a) <= float(b)
        except (TypeError, ValueError):
            return False

    # Logic operators
    def _op_and(self, args: List[Any], data: Dict[str, Any]) -> Any:
        """Logical AND - returns first falsy or last value"""
        result = True
        for arg in args:
            result = self._resolve(arg, data)
            if not result:
                return result
        return result

    def _op_or(self, args: List[Any], data: Dict[str, Any]) -> Any:
        """Logical OR - returns first truthy or last value"""
        result = False
        for arg in args:
            result = self._resolve(arg, data)
            if result:
                return result
        return result

    def _op_not(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Logical NOT"""
        if not args:
            return True
        return not self._resolve(args[0], data)

    def _op_double_not(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Double NOT (convert to boolean)"""
        if not args:
            return False
        return bool(self._resolve(args[0], data))

    def _op_if(self, args: List[Any], data: Dict[str, Any]) -> Any:
        """Conditional if/then/else"""
        i = 0
        while i < len(args) - 1:
            if self._resolve(args[i], data):
                return self._resolve(args[i + 1], data)
            i += 2
        # Return last arg as else, or None if no else
        if i < len(args):
            return self._resolve(args[i], data)
        return None

    # Data access
    def _op_var(self, args: List[Any], data: Dict[str, Any]) -> Any:
        """Access data variable by path"""
        if not args:
            return data

        path = args[0] if args else ""
        default = args[1] if len(args) > 1 else None

        if path == "":
            return data

        # Handle dot notation for nested access
        parts = str(path).split(".")
        result: Any = data

        for part in parts:
            if isinstance(result, dict):
                result = result.get(part)
                if result is None:
                    return default
            elif isinstance(result, list):
                try:
                    result = result[int(part)]
                except (ValueError, IndexError):
                    return default
            else:
                return default

        return result

    # Array operators
    def _op_in(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Check if value is in array/string"""
        if len(args) < 2:
            return False
        needle = self._resolve(args[0], data)
        haystack = self._resolve(args[1], data)
        if isinstance(haystack, (list, str)):
            return needle in haystack
        return False

    def _op_all(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Check if all items in array pass condition"""
        if len(args) < 2:
            return False
        items = self._resolve(args[0], data)
        condition = args[1]
        if not isinstance(items, list):
            return False
        return all(self.apply(condition, item) if isinstance(item, dict) else self.apply(condition, {"": item}) for item in items)

    def _op_some(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Check if any items in array pass condition"""
        if len(args) < 2:
            return False
        items = self._resolve(args[0], data)
        condition = args[1]
        if not isinstance(items, list):
            return False
        return any(self.apply(condition, item) if isinstance(item, dict) else self.apply(condition, {"": item}) for item in items)

    def _op_none(self, args: List[Any], data: Dict[str, Any]) -> bool:
        """Check if no items in array pass condition"""
        return not self._op_some(args, data)

    def _op_merge(self, args: List[Any], data: Dict[str, Any]) -> List:
        """Merge arrays"""
        result = []
        for arg in args:
            resolved = self._resolve(arg, data)
            if isinstance(resolved, list):
                result.extend(resolved)
            else:
                result.append(resolved)
        return result

    # String operators
    def _op_cat(self, args: List[Any], data: Dict[str, Any]) -> str:
        """Concatenate strings"""
        return "".join(str(self._resolve(arg, data)) for arg in args)

    def _op_substr(self, args: List[Any], data: Dict[str, Any]) -> str:
        """Get substring"""
        if not args:
            return ""
        s = str(self._resolve(args[0], data))
        start = int(self._resolve(args[1], data)) if len(args) > 1 else 0
        length = int(self._resolve(args[2], data)) if len(args) > 2 else None
        if length is not None:
            return s[start:start + length]
        return s[start:]

    # Numeric operators
    def _op_add(self, args: List[Any], data: Dict[str, Any]) -> float:
        """Addition"""
        return sum(float(self._resolve(arg, data)) for arg in args)

    def _op_subtract(self, args: List[Any], data: Dict[str, Any]) -> float:
        """Subtraction"""
        if not args:
            return 0.0
        if len(args) == 1:
            return -float(self._resolve(args[0], data))
        result = float(self._resolve(args[0], data))
        for arg in args[1:]:
            result -= float(self._resolve(arg, data))
        return result

    def _op_multiply(self, args: List[Any], data: Dict[str, Any]) -> float:
        """Multiplication"""
        result: float = 1.0
        for arg in args:
            result *= float(self._resolve(arg, data))
        return result

    def _op_divide(self, args: List[Any], data: Dict[str, Any]) -> float:
        """Division"""
        if len(args) < 2:
            return 0
        a = float(self._resolve(args[0], data))
        b = float(self._resolve(args[1], data))
        if b == 0:
            raise JsonLogicError("Division by zero")
        return a / b

    def _op_modulo(self, args: List[Any], data: Dict[str, Any]) -> float:
        """Modulo"""
        if len(args) < 2:
            return 0.0
        a = float(self._resolve(args[0], data))
        b = float(self._resolve(args[1], data))
        if b == 0:
            raise JsonLogicError("Modulo by zero")
        return a % b

    def _op_min(self, args: List[Any], data: Dict[str, Any]) -> float:
        """Minimum value"""
        values = [float(self._resolve(arg, data)) for arg in args]
        return min(values) if values else 0.0

    def _op_max(self, args: List[Any], data: Dict[str, Any]) -> float:
        """Maximum value"""
        values = [float(self._resolve(arg, data)) for arg in args]
        return max(values) if values else 0.0

    # Type operators
    def _op_missing(self, args: List[Any], data: Dict[str, Any]) -> List[str]:
        """Return list of missing variables"""
        missing = []
        for arg in args:
            var_name = self._resolve(arg, data) if isinstance(arg, dict) else arg
            if self._op_var([var_name], data) is None:
                missing.append(var_name)
        return missing

    def _op_missing_some(self, args: List[Any], data: Dict[str, Any]) -> List[str]:
        """Return missing if less than N are present"""
        if len(args) < 2:
            return []
        min_required = int(self._resolve(args[0], data))
        vars_to_check = args[1]
        if not isinstance(vars_to_check, list):
            vars_to_check = [vars_to_check]

        missing = self._op_missing(vars_to_check, data)
        present = len(vars_to_check) - len(missing)

        if present < min_required:
            return missing
        return []


# Singleton instance for convenience
_evaluator = JsonLogicEvaluator()


def jsonlogic_apply(rule: Union[Dict, List, Any], data: Optional[Dict[str, Any]] = None) -> Any:
    """
    Apply a JsonLogic rule to data (convenience function).

    Args:
        rule: The JsonLogic rule to evaluate
        data: The data context to evaluate against

    Returns:
        The result of evaluating the rule
    """
    return _evaluator.apply(rule, data)
