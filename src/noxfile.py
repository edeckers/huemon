import nox


def __load_poetry_venv(session):
    # https://stackoverflow.com/a/59904246
    session.run("poetry", "install")


@nox.session(python=False)
def tests(session):
    __load_poetry_venv(session)

    try:
        session.run(
            "pytest",
            "--cov",
            "--cov-config=../pyproject.toml",
            "--cov-report=html",
            "--cov-report=xml",
            "--junitxml=reports/junit-test-results.xml",
            *session.posargs,
        )
    finally:
        if session.interactive:
            session.run("coverage", "report")
