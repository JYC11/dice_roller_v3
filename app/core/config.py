import os
import sys

import typing


STAGE = typing.cast(
    typing.Literal[
        "local", "ci-testing", "testing", "develop", "staging", "production"
    ],
    os.getenv("STAGE"),
)


if "pytest" in sys.modules:
    STAGE = "testing"


if not STAGE:
    raise Exception("STAGE is not defined")
