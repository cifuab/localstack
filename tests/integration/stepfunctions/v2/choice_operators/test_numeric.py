from typing import Any, Final

import pytest

from tests.integration.stepfunctions.utils import is_old_provider
from tests.integration.stepfunctions.v2.choice_operators.utils import (
    create_and_test_comparison_function,
)

pytestmark = pytest.mark.skipif(
    condition=is_old_provider(), reason="Test suite for v2 provider only."
)


# TODO: test for validation errors, and boundary testing.

TYPE_COMPARISONS_VARS: Final[list[Any]] = [
    None,
    0,
    0.0,
    1,
    1.1,
    "",
    " ",
    [],
    [""],
    {},
    {"A": 0},
    False,
    True,
]


@pytest.mark.skip_snapshot_verify(
    paths=["$..loggingConfiguration", "$..tracingConfiguration", "$..previousEventId"]
)
class TestNumerics:
    def test_numeric_equals(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        type_equals = []
        for var in TYPE_COMPARISONS_VARS:
            type_equals.append((var, 0))
            type_equals.append((var, 0.0))
            type_equals.append((var, 1))
            type_equals.append((var, 1.0))

        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericEquals",
            comparisons=[*type_equals, (-0, 0), (0.0, 0), (2.22, 2.22)],
        )

    def test_numeric_equals_path(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        type_equals = []
        for var in TYPE_COMPARISONS_VARS:
            type_equals.append((var, 0))
            type_equals.append((var, 0.0))
            type_equals.append((var, 1))
            type_equals.append((var, 1.0))

        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericEqualsPath",
            comparisons=[*type_equals, (-0, 0), (0.0, 0), (2.22, 2.22)],
            add_literal_value=False,
        )

    def test_numeric_greater_than(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericGreaterThan",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
        )

    def test_numeric_greater_than_path(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericGreaterThanPath",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
            add_literal_value=False,
        )

    def test_numeric_greater_than_equals(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericGreaterThanEquals",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
        )

    def test_numeric_greater_than_equals_path(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericGreaterThanEqualsPath",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
            add_literal_value=False,
        )

    def test_numeric_less_than(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericLessThan",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
        )

    def test_numeric_less_than_path(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericLessThanPath",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
            add_literal_value=False,
        )

    def test_numeric_less_than_equals(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericLessThanEquals",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
        )

    def test_numeric_less_than_equals_path(
        self,
        aws_client,
        create_iam_role_for_sfn,
        create_state_machine,
        snapshot,
    ):
        create_and_test_comparison_function(
            aws_client.stepfunctions,
            create_iam_role_for_sfn,
            create_state_machine,
            snapshot,
            "NumericLessThanEqualsPath",
            comparisons=[(-0, 0), (0.0, 0), (0, 1), (1, 1), (1, 0), (0, 1)],
            add_literal_value=False,
        )
