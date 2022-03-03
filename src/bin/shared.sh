POETRY=`command -v poetry 2> /dev/null`
INSTALL_STAMP_PATH='.install.stamp'

function assert_poetry_exists () {
  if [ -z ${POETRY} ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
}

function p () {
  assert_poetry_exists
  ${POETRY} ${@}
}