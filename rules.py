from flask import Blueprint, request, jsonify
from models import Rule, db
import ast
import re

rule_blueprint = Blueprint('rules', __name__)

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, left={self.left}, right={self.right})"


def create_rule_ast(rule_string):
    try:
        # Replace standalone '=' with '==' without altering existing '=='
        rule_string = re.sub(r'(?<![=!<>])=(?![=])', '==', rule_string)
        
        # Replace logical operators for valid Python syntax
        rule_string = rule_string.replace(" OR ", " or ").replace(" AND ", " and ")
        
        # Parse the rule using Python's Abstract Syntax Tree (AST)
        parsed_ast = ast.parse(rule_string, mode='eval').body

        def build_node(expr):
            if isinstance(expr, ast.BoolOp):
                operator = 'AND' if isinstance(expr.op, ast.And) else 'OR'
                left = build_node(expr.values[0])
                right = build_node(expr.values[1])
                return Node("operator", operator, left, right)
            elif isinstance(expr, ast.Compare):
                left = expr.left.id
                op = expr.ops[0]
                right = expr.comparators[0]

                if isinstance(right, ast.Constant):
                    right_value = right.value
                else:
                    raise ValueError("Unsupported right operand type")

                if isinstance(op, ast.Gt):
                    condition = f"{left} > {right_value}"
                elif isinstance(op, ast.Lt):
                    condition = f"{left} < {right_value}"
                elif isinstance(op, ast.Eq):
                    condition = f"{left} == '{right_value}'"
                elif isinstance(op, ast.NotEq):
                    condition = f"{left} != '{right_value}'"
                elif isinstance(op, ast.GtE):
                    condition = f"{left} >= {right_value}"
                elif isinstance(op, ast.LtE):
                    condition = f"{left} <= {right_value}"
                else:
                    raise ValueError("Unsupported comparison operator")

                return Node("operand", condition)
            elif isinstance(expr, ast.Expr):
                return build_node(expr.value)
        
        return build_node(parsed_ast)
    
    except SyntaxError as e:
        raise ValueError(f"Invalid rule syntax: {e}")

def evaluate_rule(ast_node, data):
    def evaluate_node(node):
        if node.node_type == 'operator':
            left_result = evaluate_node(node.left)
            right_result = evaluate_node(node.right)
            if node.value == 'AND':
                return left_result and right_result
            elif node.value == 'OR':
                return left_result or right_result
        elif node.node_type == 'operand':
            condition = node.value
            if "==" in condition and "'" not in condition:
                parts = condition.split("==")
                condition = f"{parts[0]} == '{parts[1].strip()}'"
            return eval(condition, {}, data)
    
    return evaluate_node(ast_node)

@rule_blueprint.route('/create_rule', methods=['POST'])
def create_rule():
    data = request.json
    name = data.get('name')
    rule_string = data.get('rule_string')

    if not name or not rule_string:
        return jsonify({"error": "Both name and rule_string are required."}), 400

    # Check if rule string is valid
    try:
        create_rule_ast(rule_string)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_rule = Rule(name=name, rule_string=rule_string)
    db.session.add(new_rule)
    db.session.commit()
    
    return jsonify({"message": "Rule created", "id": new_rule.id}), 201

@rule_blueprint.route('/evaluate_rule/<int:rule_id>', methods=['POST'])
def evaluate_rule_api(rule_id):
    rule = db.session.get(Rule, rule_id)
    if not rule:
        return jsonify({"message": "Rule not found"}), 404

    data = request.json

    # Extract expected fields from the rule string
    expected_fields = extract_fields_from_rule(rule.rule_string)

    # Check for missing required fields
    missing_fields = [field for field in expected_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    ast_node = create_rule_ast(rule.rule_string)
    
    try:
        result = evaluate_rule(ast_node, data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"result": result}), 200

import re

def extract_fields_from_rule(rule_string):
    """
    Extracts field names (variables) from the rule string, ignoring string literals
    and logical operators.
    """
    # Pattern to match variables, but exclude anything inside quotes
    variable_pattern = r'\b[a-zA-Z_]\w*\b(?=(?:[^\'"]|\'[^\']*\'|"[^"]*")*$)'

    # Logical operators to ignore
    logical_operators = {"and", "or", "AND", "OR"}

    # Extract all potential variable names
    variables = re.findall(variable_pattern, rule_string)

    # Filter out logical operators and keep unique variable names
    return list(set(var for var in variables if var not in logical_operators))

@rule_blueprint.route('/combine_rules', methods=['POST'])
def combine_rules():
    data = request.json
    rule_ids = data.get('rule_ids')
    operator = data.get('operator', 'OR').upper()  # Get the operator from the request data, default to 'OR'

    # Validate the operator
    if operator not in ['AND', 'OR']:
        return jsonify({"message": "Invalid operator. Please choose 'AND' or 'OR'."}), 400

    # Fetch the rules based on provided IDs
    rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
    if len(rules) < 2:
        return jsonify({"message": "Need at least two rules to combine"}), 400

    # Combine the rule strings with parentheses around each rule
    combined_rule_string = f" {operator} ".join([f"({rule.rule_string})" for rule in rules])

    # Create and store the new combined rule in the database
    new_combined_rule = Rule(name=f"Combined Rule with {operator}", rule_string=combined_rule_string)
    db.session.add(new_combined_rule)
    db.session.commit()

    return jsonify({"message": "Rules combined", "id": new_combined_rule.id}), 201


@rule_blueprint.route('/rules', methods=['GET'])
def get_all_rules():
    rules = Rule.query.all()  # Retrieve all rules from the database
    rules_list = [
        {
            "id": rule.id,
            "name": rule.name,
            "rule_string": rule.rule_string
        }
        for rule in rules
    ]
    return jsonify(rules_list), 200

@rule_blueprint.route('/edit_rule/<int:rule_id>', methods=['PUT'])
def edit_rule(rule_id):
    # Fetch the rule from the database
    rule = db.session.get(Rule, rule_id)
    
    if not rule:
        return jsonify({"message": "Rule not found"}), 404

    # Get the updated rule string from the request
    data = request.json
    new_rule_string = data.get('rule_string')

    if not new_rule_string:
        return jsonify({"error": "New rule_string is required."}), 400

    # Check if the new rule string is valid by attempting to parse it into an AST
    try:
        create_rule_ast(new_rule_string)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Update the rule string
    rule.rule_string = new_rule_string

    # Commit changes to the database
    db.session.commit()

    return jsonify({"message": "Rule updated successfully", "id": rule.id}), 200
