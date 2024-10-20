import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Rule
from rules import rule_blueprint, create_rule_ast, evaluate_rule
import json

class TestRules(unittest.TestCase):
    def setUp(self):
        """Set up a test client and create an in-memory SQLite database."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.register_blueprint(rule_blueprint)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_individual_rules(self):
        """Test creation of individual rules and verify their AST representation."""
        rule_strings = [
            "age > 18",
            "status == 'active'",
            "score >= 75 AND category == 'A'"
        ]

        for rule_string in rule_strings:
            response = self.client.post('/create_rule', json={
                'name': f'Test Rule: {rule_string}',
                'rule_string': rule_string
            })
            self.assertEqual(response.status_code, 201)

            # Verify AST representation
            ast = create_rule_ast(rule_string)
            self.assertIsNotNone(ast)
            print(f"Created rule: {rule_string}")
            print(f"AST: {ast}")
            print("----")

    def test_combine_rules(self):
        """Test combining two individual rules into one."""
        # Create individual rules
        rule1 = self.client.post('/create_rule', json={
            'name': 'Rule 1',
            'rule_string': 'age > 18'
        }).get_json()
        rule2 = self.client.post('/create_rule', json={
            'name': 'Rule 2',
            'rule_string': 'status == "active"'
        }).get_json()

        # Combine rules
        response = self.client.post('/combine_rules', json={
            'rule_ids': [rule1['id'], rule2['id']],
            'operator': 'AND'
        })
        self.assertEqual(response.status_code, 201)

        # Verify combined rule
        combined_rule_id = response.get_json()['id']
        with self.app.app_context():
            combined_rule = db.session.get(Rule, combined_rule_id)
            self.assertIsNotNone(combined_rule)
            self.assertEqual(combined_rule.rule_string, '(age > 18) AND (status == "active")')
            print(f"Combined rule: {combined_rule.rule_string}")
            print("----")

    def test_evaluate_rule(self):
        """Test the evaluation of a specific rule against various data inputs."""
        # Create a rule
        rule_response = self.client.post('/create_rule', json={
            'name': 'Test Evaluation Rule',
            'rule_string': 'age >= 18 AND status == "active"'
        })
        rule_id = rule_response.get_json()['id']

        # Test cases
        test_cases = [
            ({'age': 20, 'status': 'active'}, True),
            ({'age': 17, 'status': 'active'}, False),
            ({'age': 18, 'status': 'inactive'}, False),
            ({'age': 25, 'status': 'active'}, True)
        ]
        for data, expected_result in test_cases:
            response = self.client.post(f'/evaluate_rule/{rule_id}', json=data)
            self.assertEqual(response.status_code, 200)
            result = response.get_json()['result']
            print(f"Rule: age >= 18 AND status == 'active'")
            print(f"Data: {data}")
            print(f"Expected: {expected_result}, Actual: {result}")
            self.assertEqual(result, expected_result)
            print("----")

    def test_combine_multiple_rules(self):
        """Test combining multiple pairs of rules and evaluate each combined rule."""
        # Create individual rules
        rule1 = self.client.post('/create_rule', json={
            'name': 'Rule 1',
            'rule_string': 'age > 18'
        }).get_json()
        rule2 = self.client.post('/create_rule', json={
            'name': 'Rule 2',
            'rule_string': 'status == "active"'
        }).get_json()

        # Combine rules in pairs
        combinations = [
            ([rule1['id'], rule2['id']], 'OR')
        ]

        for rule_ids, operator in combinations:
            response = self.client.post('/combine_rules', json={
                'rule_ids': rule_ids,
                'operator': operator
            })
            self.assertEqual(response.status_code, 201)

            # Verify combined rule
            combined_rule_id = response.get_json()['id']
            with self.app.app_context():
                combined_rule = db.session.get(Rule, combined_rule_id)
                self.assertIsNotNone(combined_rule)

                # Create the expected rule string
                combined_rule_string = f'{" OR ".join([f"({db.session.get(Rule, rid).rule_string})" for rid in rule_ids])}'
                self.assertEqual(combined_rule.rule_string, combined_rule_string)
                print(f"Combined rule: {combined_rule.rule_string}")

            # Test evaluation of combined rule
            test_cases = [
                ({'age': 20, 'status': 'inactive', 'score': 70}, True),
                ({'age': 17, 'status': 'active', 'score': 60}, True),
                ({'age': 16, 'status': 'active', 'score': 80}, True), 
                ({'age': 16, 'status': 'inactive', 'score': 70}, False),
            ]
            for data, expected_result in test_cases:
                response = self.client.post(f'/evaluate_rule/{combined_rule_id}', json=data)
                self.assertEqual(response.status_code, 200)
                result = response.get_json()['result']

                print(f"Rule: {combined_rule.rule_string}")
                print(f"Data: {data}")
                print(f"Expected: {expected_result}, Actual: {result}")

                # Evaluate each part of the combined rule separately
                rule_parts = [
                    ('age > 18', data['age'] > 18),
                    ('status == "active"', data['status'] == 'active'),
                    ('score >= 75', data['score'] >= 75)
                ]

                for rule_part, part_result in rule_parts:
                    print(f"  Evaluating: {rule_part} = {part_result}")
                print(f"Final result: {result}")
                print("----")
                self.assertEqual(result, expected_result, f"Failed for data: {data}")

if __name__ == '__main__':
    unittest.main()
