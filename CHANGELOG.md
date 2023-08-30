# CHANGELOG



## v1.0.2 (2023-08-30)

### Fix

* fix(deps): bump python-semantic-release to ^8.0.0 ([`1aa06ae`](https://github.com/edeckers/huemon/commit/1aa06aeb42169234c721422e856aa1a4cfe6724b))

* fix(deps): bump dependencies ([`769b3ba`](https://github.com/edeckers/huemon/commit/769b3baae9a99f89e787680a2e00433b0d0b59c9))


## v1.0.1 (2023-02-08)

### Ci

* ci(deps): bump pre-commit dependencies ([`f21daa3`](https://github.com/edeckers/huemon/commit/f21daa3d1e089e8433a0d76520b9631fbd8ea2b1))

### Fix

* fix(deps): bump all dependencies (#60) ([`bda097b`](https://github.com/edeckers/huemon/commit/bda097b4bff27b9cbf94540f8ef9410a78fa8696))

* fix: typo in container registry domain (#59) ([`340fdde`](https://github.com/edeckers/huemon/commit/340fdde172a0961c5bd1a0302aa9910c909aad3e))


## v1.0.0 (2022-10-15)

### Breaking

* fix(deps): replace monads with pyella

The monad sources were migrated to the pyella library, so replace the
sources with said library. Pyella only supports Python &gt;= 3.8 though,
because everything older is ancient, which is why Huemon will make the same change.

BREAKING CHANGE: minimal python version bumped to 3.8 ([`cedae55`](https://github.com/edeckers/huemon/commit/cedae5530a252996ff0f60bfcce567ed5b8fb730))

### Documentation

* docs: fix a few mistakes ([`1edf838`](https://github.com/edeckers/huemon/commit/1edf838ba2c6a2c731c28ad66d37065a19f98d51))

### Fix

* fix(deps): update all dependencies ([`9b8bdcb`](https://github.com/edeckers/huemon/commit/9b8bdcb4fb268d86627164819bd8558fa1cf48da))

* fix(deps): use modern (1.2.2) poetry installer ([`e97cb13`](https://github.com/edeckers/huemon/commit/e97cb137f573e3298a7882b1f13f313e24debefb))


## v0.9.2 (2022-07-28)

### Ci

* ci: add triggers for running tests ([`18d2c84`](https://github.com/edeckers/huemon/commit/18d2c8488166f4ae904b694e40c0e7c2e019ec9e))

### Documentation

* docs: move code of conduct to separate file ([`c8b64d6`](https://github.com/edeckers/huemon/commit/c8b64d61fdc763000ce7766dcd599a88d6b42bdf))

### Fix

* fix: release fails because of missing history ([`b139fea`](https://github.com/edeckers/huemon/commit/b139fea2783414bc94d349f989ebb009677469f9))

* fix: change path to bridge update status (#58) ([`c55f1f0`](https://github.com/edeckers/huemon/commit/c55f1f09f91ef71d7725bbd3bbe3824679b3e795))


## v0.9.1 (2022-03-28)

### Fix

* fix: missing ghcr.io prefix in release script ([`aa219f6`](https://github.com/edeckers/huemon/commit/aa219f6a06dfb4ad140a22967a78c92a31d2ec50))


## v0.9.0 (2022-03-28)

### Breaking

* fix: release image to ghrc.io (#57)

BREAKING CHANGE:
Images are now released through ghrc.io instead of DockerHub ([`c0709af`](https://github.com/edeckers/huemon/commit/c0709afd7713219bd07e7556b56e3c30aa8e0c0b))


## v0.8.0 (2022-03-22)

### Refactor

* refactor: split and reorder code (#56) ([`8205f29`](https://github.com/edeckers/huemon/commit/8205f29759166116ad19626318a1071b0b778242))


## v0.7.5 (2022-03-11)

### Fix

* fix: discovery plugin system (#54)

* fix: docker image build

* fix: hardwire discoveries

* fix: load discovery plugins only once

* chore: change plugin configuration path ([`f219022`](https://github.com/edeckers/huemon/commit/f219022822cd030ff9c2aa3c6a93ed26eea2c7f2))


## v0.7.4 (2022-03-11)

### Chore

* chore: make git release user info configurable (#51)

* chore: make git release user info configurable

* chore: change protected GITHUB prefix to GH ([`57cec5d`](https://github.com/edeckers/huemon/commit/57cec5d94097675f8893a9be4862fdf43fea5d67))

### Fix

* fix: hard-wire provided commands (#53) ([`ce37410`](https://github.com/edeckers/huemon/commit/ce37410eb4d3b0db5997931e04f92321651db88b))

### Refactor

* refactor: rename Zabbix triggers and items (#52) ([`3767bf6`](https://github.com/edeckers/huemon/commit/3767bf633a60059d01b36673724d42f6570a82cc))


## v0.7.3 (2022-03-10)

### Chore

* chore: add Docker Hub credentials to workflow (#47) ([`b0544e7`](https://github.com/edeckers/huemon/commit/b0544e747f78babd7f2e472b35bdadb4880a8be3))

### Ci

* ci: add release workflow (#45) ([`299f79c`](https://github.com/edeckers/huemon/commit/299f79cbffbb684ce124bcaeea0c75daceea9d0d))

* ci: add dummy release workflow (#46) ([`da925f4`](https://github.com/edeckers/huemon/commit/da925f4d838266434297bab49e8d645ef100114b))

### Fix

* fix: remove superfluous publish parameter (#50) ([`6a4f6f7`](https://github.com/edeckers/huemon/commit/6a4f6f740d2889be193558662722f9593bfa6bc4))

* fix: set release git details (#49) ([`8583f01`](https://github.com/edeckers/huemon/commit/8583f019d532a137d2a48f54b709da76918e79b7))

* fix: make release check (#48) ([`e93b504`](https://github.com/edeckers/huemon/commit/e93b504d4360105b0a1b587ceedc768cebe85ef6))


## v0.7.2 (2022-03-10)

### Fix

* fix: reads from other thread stdout (#44) ([`3a1edbe`](https://github.com/edeckers/huemon/commit/3a1edbe75920f677be8e7f72588680e0349788b9))


## v0.7.1 (2022-03-09)

### Fix

* fix: separate prod and dev dependencies (#40) ([`91b0855`](https://github.com/edeckers/huemon/commit/91b08556566d14f750d2457f0d2374b7460de568))


## v0.7.0 (2022-03-09)

### Feature

* feat: add agent mode (#38)

* chore: add basics for fastapi command

* chore: add hardcoded discover request

* chore: add parameters to discover request

* chore: add dynamic routes for all commands

* refactor: wrap server code in class

* chore: add license headers

* chore: add agent command to docker

* chore: add agent command to README.md

* chore: improve docker support

* fix: filter empty request parameters

* docs: update docker information in README.md

* chore: add huemon systemd service

* chore: add Systemd installer and documentation

* chore: reorganize Dockerfile

* chore: replace version in Dockerfile

* chore: change version in docker-compose.yml

* chore: add release script ([`3741861`](https://github.com/edeckers/huemon/commit/374186124ef4c4cf4b9767bcbced14608e21899c))

### Fix

* fix: release script (#39) ([`d0947e9`](https://github.com/edeckers/huemon/commit/d0947e95c76037253278d9ae1c7fd70b2761b882))


## v0.6.0 (2022-03-07)

### Chore

* chore: extend coverage (#36)

* chore: test locked method

* chore: fix typo

* chore: cover locked call fully

* chore: cover parameter assertions ([`3630504`](https://github.com/edeckers/huemon/commit/3630504c96477a438aa1ac24b9deb6b1469a3e36))

### Ci

* ci: add active Python versions to test matrix (#37)

* ci: add active Python versions to test matrix

* chore: replace magic wait time with semaphore

* chore: replace read_result with mock assertions ([`c89b485`](https://github.com/edeckers/huemon/commit/c89b48543bb74f0b87e1aac729f4fa9221c4640f))


## v0.5.0 (2022-03-06)

### Chore

* chore: extend test set (#35)

* chore: add a few tests for light command

* chore: test all light commands

* chore: test unkown light mac

* chore: add battery:level tests

* chore: add light:level tests

* chore: add sensor:presence tests

* chore: add sensor:temperature tests

* chore: add system:* tests

* chore: cover all off api_factory

* chore: add tests for cached api ([`56e7610`](https://github.com/edeckers/huemon/commit/56e7610768d85f87f0cbc2fa04c150ed158a47cb))

* chore: add code coverage (#34)

* chore: add code coverage

* chore: source env when available

* chore: fix report archivation ([`8c8021e`](https://github.com/edeckers/huemon/commit/8c8021eb1f07c1f6ed9c1db2b97f6bf0cf1c4f9e))


## v0.4.0 (2022-03-05)

### Documentation

* docs: add PyPI badge (#28) ([`69f7f68`](https://github.com/edeckers/huemon/commit/69f7f684d56861c7686cb593b152a1f9f83849b5))


## v0.3.0 (2022-03-05)

### Documentation

* docs: use absolute urls to screenshots (#27) ([`2fd701e`](https://github.com/edeckers/huemon/commit/2fd701ef9c797eb5189a160028228886c13acad7))


## v0.2.0 (2022-03-05)

### Documentation

* docs: add screenshots (#26) ([`f1281b4`](https://github.com/edeckers/huemon/commit/f1281b442619c03b29d7df1c50795bf2a1dea625))


## v0.1.0 (2022-03-05)

### Chore

* chore: change release git subject (#25) ([`9f227e8`](https://github.com/edeckers/huemon/commit/9f227e884646e29872154440865ee23f44591248))

* chore: improve release configuration (#24) ([`16cdea5`](https://github.com/edeckers/huemon/commit/16cdea5a7492a4ced0b0ac9e4d5543db943a9c69))

* chore: reset version number to 0.0.0 (#23) ([`6dc1228`](https://github.com/edeckers/huemon/commit/6dc1228f025865eb87179fd7529eb73fd01dc77d))

* chore: repare for release (#22)

* chore: prepare for release on pypy

* chore: add semantic-release ([`07f983e`](https://github.com/edeckers/huemon/commit/07f983e57002651dd1e17310ae3e46fd7a8941ac))

* chore: add Docker configuration (#20)

* chore: add Docker configuration

* chore: change env to arg

* chore: change a few docker related scripts

* chore: add attribution and license headers

* chore: unset x

* chore: change and remove a few words ([`62781c9`](https://github.com/edeckers/huemon/commit/62781c9d3ccb0b3dedfb03002701acd788375f93))


## v0.0.3 (2022-03-04)

### Chore

* chore: add project metadata (#21) ([`aec39e8`](https://github.com/edeckers/huemon/commit/aec39e80f5dbd6979ffa6621de8dd1b2ff05d01b))

* chore: add poetry (#18)

* chore: add poetry

* refactor: extend Makefile with targets

* chore: expand pyproject config

* chore: add mypy type checking

* style: add newline to ends of files ([`c405594`](https://github.com/edeckers/huemon/commit/c405594467be7437b1ff2fe27ab80f638bffebed))

### Feature

* feat: add nox and remove superfluous files (#19)

* feat: add nox and remove setup.py

* ci: add test GitHub workflow

* chore: add test reporting

* chore: publish test result ([`5c03dc5`](https://github.com/edeckers/huemon/commit/5c03dc502b3f1e26de20cbbf6da4770afcdd3220))

### Style

* style: add pre-commit hooks (#17)

* Add pre-commit hook

* feat: add commit linter

* feat: add gitlint pre-commit hook

* feat: add black pre-commit hook

* feat: add bandit hook

* style: add isort commit hook

* style: apply all pre-commit hooks ([`06993d8`](https://github.com/edeckers/huemon/commit/06993d8251349b6650a2e57ba7787bbeb31b0e4f))


## v0.0.2 (2022-02-28)

### Unknown

* Bump version to 0.0.2 ([`d155da5`](https://github.com/edeckers/huemon/commit/d155da5b31b9c565e9a0aad94f6c9455718bfda4))

* Add tests (#16) ([`9052d50`](https://github.com/edeckers/huemon/commit/9052d50cb066a82fb560dad1e9228b356613a135))

* Fix broken system command (#15) ([`1c6a774`](https://github.com/edeckers/huemon/commit/1c6a77443a09e6dc924cdca9d384a8b433c7d71b))

* Change LightCommand to self (#14) ([`52f4844`](https://github.com/edeckers/huemon/commit/52f48444d4c78691491465298e772032cc28e828))

* Improve code quality (#13)

* Replace magic error codes with consts

* Replace al erroneous exits with exit_fail

* Remove unused imports

* Use consts and exit_fail on sensors_discovery

* Replace all LOG.error with exit_fail

* inline some single use constants

* Interpolate Command::name in log messages

* Add number of arguments assertion

* Add value exists assertion ([`f3dfd2a`](https://github.com/edeckers/huemon/commit/f3dfd2a3b7f07366313920dbdddbfe79a479365c))

* Fix small inconsistencies (#12) ([`8a48f27`](https://github.com/edeckers/huemon/commit/8a48f27cf393fed33d4c37652116c9366bdd289c))

* Add missing command and discovery directories (#11) ([`bec7b44`](https://github.com/edeckers/huemon/commit/bec7b4489d35f71c0b8e64f4d998b896175c60cd))


## v0.0.1 (2022-02-27)

### Unknown

* Change Zabbix example template (#10) ([`58e3729`](https://github.com/edeckers/huemon/commit/58e37296dfc01a74fdb9f5a3fa4a4f0d25764e74))

* Add contribution guidelines and code of conduct (#9)

* Add contribution guidelines and code of conduct

* Add some GitHub issue templates ([`34fcb25`](https://github.com/edeckers/huemon/commit/34fcb254aba044883104d20b7345616628940205))

* Inject configuration to instead of hard-code (#8)

* Inject configuration to Discovery

* Inject configuration instead of hard-code ([`58dad7a`](https://github.com/edeckers/huemon/commit/58dad7acba379300eccbae091134e95f5c1cdb2e))

* Make API caching configurable (#7) ([`1029fe3`](https://github.com/edeckers/huemon/commit/1029fe37e628f62b1b0b9de75f385d66973182c7))

* Improve documentation regarding config files (#6) ([`640f0a3`](https://github.com/edeckers/huemon/commit/640f0a3081522004cac226358c3e56c5d3408a84))

* Make config path configurable (#5)

* Make config path configurable

* Update README.md with configuration instructions

* Rename HueMon to huemon in setup.py

* Add commands and discoveries to setup.py

* Add license information to setup.py

* Add install_available command

* Add new fields to config.example.yml

* Reflect configuration changes in README.md ([`130d534`](https://github.com/edeckers/huemon/commit/130d5341cd81a15b76152eb5dcf3222d4e15de6f))

* Rename module to huemon (#4) ([`ecf4cd1`](https://github.com/edeckers/huemon/commit/ecf4cd195e0f15f22a9aec6c0b2ac3f66eba886a))

* Apply some code hygiene (#3)

* Move script to modules and add requirements.txt

* Fix all linter errors

* Add build script

* Add Makefile

* Add relevant information to README.md

* Add license headers ([`aa78433`](https://github.com/edeckers/huemon/commit/aa7843313e7f6112b806115cd363901d16d88ebe))

* Refactor discoveries to plugins (#2)

* Refactor to separate discovery classes

* Move discovery handlers to files

* Exclude discoveries_enabled directory

* Load discoveries dynamically ([`51f4219`](https://github.com/edeckers/huemon/commit/51f4219c3206b527f0aee73740cd89ad2f27918d))

* Refactor to command plugin architecture (#1)

* Refactor to SystemCommand

* Refactor to LightCommand

* Refactor to Sensor- and DiscoverCommands

* Move interfaces to separate files

* Split Apis to separate modules

* Move commands to separate files

* Load commands from commands_enabled path

* Move plugin code to separate module ([`c582917`](https://github.com/edeckers/huemon/commit/c582917350fe1f09b85821ab9a8435401274326a))

* Fix sensor incorrect parameter bug ([`ae23fb7`](https://github.com/edeckers/huemon/commit/ae23fb79214ace5247c6ef9d0b1d8c5a2c707920))

* Make cache age configurable ([`07693c8`](https://github.com/edeckers/huemon/commit/07693c868bb977a2f2cf13375eb1fa10485d8183))

* Fix cache seconds vs ms and cache per type ([`c85d9e4`](https://github.com/edeckers/huemon/commit/c85d9e4d4c3b6db82ec82e15cdafa1c6d73a6a50))

* Add simple and basic caching for api ([`4da0697`](https://github.com/edeckers/huemon/commit/4da06972d506fc9eaed85bf6ac4501a745e73e7a))

* Add some logging to Api ([`aa3046d`](https://github.com/edeckers/huemon/commit/aa3046df6f935f625040b15193da7382ec892411))

* Add basics for cached api ([`a6725e4`](https://github.com/edeckers/huemon/commit/a6725e403461295e1d665f4c271d28fc19477806))

* Verify correct number of arguments ([`11b524b`](https://github.com/edeckers/huemon/commit/11b524baf601ddf821d1733c02af137829a4b77f))

* Fix usage of correct path for config read ([`e00b380`](https://github.com/edeckers/huemon/commit/e00b3801b276afcec271dc41ddb625e6d1b7b7bd))

* Add logging and read config from yaml ([`4c07c56`](https://github.com/edeckers/huemon/commit/4c07c565bfa3d34fb830f45ee5485d83b12873b3))

* Fix a few styling issues ([`07ce52c`](https://github.com/edeckers/huemon/commit/07ce52c74b9d242279fb04fe233e5230a1842d8c))

* Inline a few single line methods ([`2c7240e`](https://github.com/edeckers/huemon/commit/2c7240e39bb5c3860c210e3d53e9266aa22c44c1))

* Inline a couple of short methods ([`8d81d63`](https://github.com/edeckers/huemon/commit/8d81d6305d423a0fbb0a487a6573ddc4bb0e67b2))

* Remove hardcoded command handling ([`fd0c4b1`](https://github.com/edeckers/huemon/commit/fd0c4b1e1dac3a4f796afd898a99b75fc1dcaa2d))

* Simplify lights output ([`5d2d5a3`](https://github.com/edeckers/huemon/commit/5d2d5a39169e7aab4eefd951646fcf4be0ccc888))

* Simplify discovery output ([`9910c5c`](https://github.com/edeckers/huemon/commit/9910c5c0a11cdafe72bb0b7fbdfe7634987f94ee))

* Simplify field retrieval ([`9d94670`](https://github.com/edeckers/huemon/commit/9d94670c3835b87d924d495eda2be467ecebfb47))

* Wrap code in classes ([`8b3659b`](https://github.com/edeckers/huemon/commit/8b3659b54317438d6a4f2e8a85be3d42d6b2e566))

* Simplify some discoveries ([`39763f9`](https://github.com/edeckers/huemon/commit/39763f966f75f3365187af295c713f1ec5c4e4b5))

* Add Zabbix template and sample config ([`f7ad7a8`](https://github.com/edeckers/huemon/commit/f7ad7a817addebbde3b49593193592973f089fb4))

* Add some sensor values ([`bb839de`](https://github.com/edeckers/huemon/commit/bb839dedac07c091020f029bc9bf7ca7a109d5c9))

* Add quick and dirty light and battery discovery ([`733070d`](https://github.com/edeckers/huemon/commit/733070dc562d3ec33029a3fad03a7f68c7c5a440))

* Initial commit ([`f383eb0`](https://github.com/edeckers/huemon/commit/f383eb040e30b0579e3344062a888c375206d243))
