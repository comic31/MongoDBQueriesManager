from __future__ import annotations

import nox

from nox import Session


PYTHONS_TESTS = ["3.7", "3.8", "3.9", "3.10", "3.11"]
PYTHONS_BASE = ["3.10"]
nox.options.reuse_existing_virtualenvs = False


@nox.session(python=PYTHONS_TESTS)
def tests(session: Session) -> None:
    # Create reports folder for pytest & coverage
    session.run("mkdir", "-p", f"reports/pytest/{session.name}", external=True)
    session.run("mkdir", "-p", f"reports/coverage/{session.name}", external=True)

    # Remove pytest cache directory
    session.run("rm", "-fr", ".pytest_cache", external=True)

    # Install tests dependencies
    session.install("pytest", "coverage", "pymongo")

    # Run pytest without dateparser
    session.run(
        "coverage",
        "run",
        f"--data-file=./reports/coverage/{session.name}/.coverage",
        "-m",
        "pytest",
        f"--junitxml=./reports/pytest/{session.name}/junit.xml"
        f"--junit-prefix={session.name}",
        "-vv",
    )

    # Install dateparser extra dep
    session.install("dateparser")

    # Run pytest with dateparser
    session.run(
        "coverage",
        "run",
        f"--data-file=./reports/coverage/{session.name}/.coverage.extra",
        "-m",
        "pytest",
        f"--junitxml=./reports/pytest/{session.name}/junit-extra.xml"
        f"--junit-prefix={session.name}",
        "-vv",
    )

    # Combine coverage
    session.run(
        "coverage",
        "combine",
        "--append",
        f"--data-file=./reports/coverage/{session.name}/.coverage.full",
        f"./reports/coverage/{session.name}/.coverage",
        f"./reports/coverage/{session.name}/.coverage.extra",
    )

    # Generate coverage HTML result
    session.run(
        "coverage",
        "html",
        f"--data-file=./reports/coverage/{session.name}/.coverage.full",
        f"--directory=./reports/coverage/{session.name}/html",
    )

    # Generate coverage XML result
    session.run(
        "coverage",
        "xml",
        f"--data-file=./reports/coverage/{session.name}/.coverage.full",
        f"-o ./reports/coverage/{session.name}/coverage-{session.name}-full.xml",
    )

    # Display coverage report
    session.run(
        "coverage",
        "report",
        f"--data-file=./reports/coverage/{session.name}/.coverage.full",
    )


@nox.session(python=PYTHONS_BASE)
def lints(session: Session) -> None:
    # Create reports folder for flake8
    session.run("mkdir", "-p", f"reports/flake8/{session.name}", external=True)

    # Install lints dependencies
    session.install("pylint", "flake8>=4.0.0,<5.0.0", "flake8-html==0.4.2")

    # Run flake8
    session.run(
        "flake8",
        "mongo_queries_manager",
        "--format=html",
        f"--htmldir=./reports/flake8/{session.name}",
    )

    # Run pylint
    session.run("pylint", "mongo_queries_manager")


@nox.session(python=PYTHONS_BASE)
def formats(session: Session) -> None:
    # Install formats dependencies
    session.install("black", "isort")

    # Run black
    session.run("black", "mongo_queries_manager", "--check")

    # Run isort
    session.run("isort", "mongo_queries_manager", " --check")


@nox.session(python=PYTHONS_BASE)
def types(session: Session) -> None:
    # Install types dependencies
    session.install("dateparser", "mypy", "types-dateparser")

    # Remove mypy cache directory
    session.run("rm", "-fr", ".mypy_cache", external=True)

    # Run mypy
    session.run("mypy", "mongo_queries_manager")
