import ast
import operator
from data import ASSIGNMENTS


# --------------------------------------------------
# TOOL 1: Get assignment information
# --------------------------------------------------

def get_assignment_info(assignment_name=None, status=None):
    results = ASSIGNMENTS

    if assignment_name:
        results = [
            assignment
            for assignment in results
            if assignment["name"].lower() == assignment_name.lower()
        ]

    if status:
        results = [
            assignment
            for assignment in results
            if assignment["status"].lower() == status.lower()
        ]

    return results


# --------------------------------------------------
# TOOL 2: Safe calculator
# --------------------------------------------------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_calculate(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = OPERATORS.get(type(node.op))

            if operation:
                return operation(left, right)

        raise ValueError("Unsupported expression")

    return evaluate(tree)


# --------------------------------------------------
# OpenAI-compatible tool definitions
# --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_assignment_info",
            "description": (
                "Retrieve private assignment information such as "
                "assignment name, subject, status, and due date."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "assignment_name": {
                        "type": "string",
                        "description": "Exact assignment name if known."
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status such as Pending or Completed."
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform basic arithmetic calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression to calculate."
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    }
]


TOOL_FUNCTIONS = {
    "get_assignment_info": get_assignment_info,
    "calculator": safe_calculate
}


# --------------------------------------------------
# Simple tool test
# --------------------------------------------------

if __name__ == "__main__":
    print("Assignment lookup:")
    print(get_assignment_info(assignment_name="Python Recursion"))

    print("\nPending assignments:")
    print(get_assignment_info(status="Pending"))

    print("\nCalculator:")
    print(safe_calculate("2 + 3 * 4"))