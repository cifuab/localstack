import os
from typing import Final

from tests.integration.stepfunctions.templates.template_loader import TemplateLoader

_THIS_FOLDER: Final[str] = os.path.dirname(os.path.realpath(__file__))


class ErrorHandlingTemplate(TemplateLoader):

    # State Machines.
    AWS_SDK_TASK_FAILED_S3_LIST_OBJECTS: Final[str] = os.path.join(
        _THIS_FOLDER, "statemachines/aws_sdk_task_error_s3_list_objects.json5"
    )

    AWS_SDK_TASK_FAILED_SECRETSMANAGER_CREATE_SECRET: Final[str] = os.path.join(
        _THIS_FOLDER, "statemachines/aws_sdk_task_error_secretsmanager_crate_secret.json5"
    )

    AWS_LAMBDA_INVOKE_CATCH_UNKNOWN: Final[str] = os.path.join(
        _THIS_FOLDER, "statemachines/task_lambda_invoke_catch_unknown.json5"
    )

    AWS_LAMBDA_INVOKE_CATCH_RELEVANT: Final[str] = os.path.join(
        _THIS_FOLDER, "statemachines/task_lambda_invoke_catch_relevant.json5"
    )

    AWS_SERVICE_LAMBDA_INVOKE_CATCH_UNKNOWN: Final[str] = os.path.join(
        _THIS_FOLDER, "statemachines/task_service_lambda_invoke_catch_unknown.json5"
    )

    AWS_SERVICE_LAMBDA_INVOKE_CATCH_RELEVANT: Final[str] = os.path.join(
        _THIS_FOLDER, "statemachines/task_service_lambda_invoke_catch_relevant.json5"
    )

    AWS_SERVICE_SQS_SEND_MSG_CATCH: Final[str] = os.path.join(
        _THIS_FOLDER, "statemachines/task_service_sqs_send_msg_catch.json5"
    )

    # Lambda Functions.
    LAMBDA_FUNC_RAISE_EXCEPTION: Final[str] = os.path.join(
        _THIS_FOLDER, "lambdafunctions/raise_exception.py"
    )
