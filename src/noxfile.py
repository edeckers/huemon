import nox


@nox.session
def tests(session):
    session.install("pytest")
    session.run("pytest", "--quiet", "--junitxml=reports/junit-test-results.xml")
