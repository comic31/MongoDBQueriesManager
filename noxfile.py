from __future__ import annotations

import nox
from nox import Session

PYTHONS_TESTS = ["3.10", "3.11", "3.12", "3.13", "3.14"]
PYTHONS_BASE = ["3.14"]
nox.options.reuse_existing_virtualenvs = False


REPORT_PATH = "reports/"
PYTEST_REPORT_PATH = REPORT_PATH + "pytest/"
COVERAGE_REPORT_PATH = REPORT_PATH + "coverage/"


@nox.session(python=PYTHONS_TESTS)
def tests(session: Session) -> None:
    # Create reports folder for pytest & coverage
    session.run("mkdir", "-p", f"{PYTEST_REPORT_PATH}{session.name}", external=True)
    session.run("mkdir", "-p", f"{COVERAGE_REPORT_PATH}{session.name}", external=True)

    # Remove pytest cache directory
    session.run("rm", "-fr", ".pytest_cache", external=True)

    # Install tests dependencies
    session.install("pytest", "coverage", "pymongo")

    # Run pytest without dateparser
    session.run(
        "coverage",
        "run",
        f"--data-file={COVERAGE_REPORT_PATH}{session.name}/.coverage",
        "-m",
        "pytest",
        f"--junitxml={PYTEST_REPORT_PATH}{session.name}/junit.xml",
        f"--junit-prefix={session.name}",
        "-vv",
    )

    # Install dateparser extra dep
    session.install("dateparser")

    # Run pytest with dateparser
    session.run(
        "coverage",
        "run",
        f"--data-file={COVERAGE_REPORT_PATH}{session.name}/.coverage.extra",
        "-m",
        "pytest",
        f"--junitxml={PYTEST_REPORT_PATH}{session.name}/junit-extra.xml",
        f"--junit-prefix={session.name}",
        "-vv",
    )

    # Combine coverage
    session.run(
        "coverage",
        "combine",
        "--append",
        f"--data-file={COVERAGE_REPORT_PATH}{session.name}/.coverage.full",
        f"{COVERAGE_REPORT_PATH}{session.name}/.coverage",
        f"{COVERAGE_REPORT_PATH}{session.name}/.coverage.extra",
    )

    # Generate coverage HTML result
    session.run(
        "coverage",
        "html",
        f"--data-file={COVERAGE_REPORT_PATH}{session.name}/.coverage.full",
        f"--directory={COVERAGE_REPORT_PATH}{session.name}/html",
    )

    # Generate coverage XML result
    session.run(
        "coverage",
        "xml",
        f"--data-file={COVERAGE_REPORT_PATH}{session.name}/.coverage.full",
        "-o",
        f"{COVERAGE_REPORT_PATH}{session.name}/coverage-{session.name}-full.xml",
    )

    # Display coverage report
    session.run(
        "coverage",
        "report",
        f"--data-file={COVERAGE_REPORT_PATH}{session.name}/.coverage.full",
    )


@nox.session(python=PYTHONS_BASE)
def lints(session: Session) -> None:
    # Install lints dependencies
    session.install("ruff")

    # Run ruff
    session.run("ruff", "check", "mongo_queries_manager")


@nox.session(python=PYTHONS_BASE)
def formats(session: Session) -> None:
    # Install formats dependencies
    session.install("ruff")

    # Run black
    session.run("ruff", "format", "--check", "mongo_queries_manager")


@nox.session(python=PYTHONS_BASE)
def types(session: Session) -> None:
    # Install types dependencies
    session.install("dateparser", "mypy", "types-dateparser")

    # Remove mypy cache directory
    session.run("rm", "-fr", ".mypy_cache", external=True)

    # Run mypy
    session.run("mypy", "mongo_queries_manager")
