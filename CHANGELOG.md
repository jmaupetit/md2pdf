# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added 

- CLI: add `--watch` option

### Fixed

- Docker: fix fontconfig warning message by settings `/tmp` as home directory

## [3.0.1] - 2026-01-27

### Fixed 

- Docker: add missing extra dependencies

## [3.0.0] - 2026-01-22

### Added 

- CLI: allow multiple input markdown files (converted using multiple threads)
- CLI: add the `--workers` option to adapt parallelisation

### Changed

- Add dependency groups to handle project flavors (`cli` and `latex`) [BC]
- CLI: switched to [Typer](https://typer.tiangolo.com/)
- CLI: moved to a no-arguments command (only options) [BC]

## [2.1.0] - 2026-01-12

### Added

- Allow extra markdown extensions configuration using a JSON string (CLI) or a
  dict (API)

## [2.0.0] - 2026-01-09

### Added

- Add an Alpine Linux lightweight Docker image
- Consider every input markdown source as a Jinja template

### Changed

- Switch to `uv` for packaging and dependency management
- Add extra extensions to the default extensions list

### Removed

- Drop support for python < 3.10

## [1.0.1] - 2023-04-12

### Fixed

- Fix md2pdf module loading during installation

## [1.0.0] - 2023-04-12

### Fixed 

- Fix installation issue

### Removed

- Drop support for python < 3.8

## [0.6] - 2023-04-07

### Added

- Add markdown footnotes support

### Fixed

- Fix package entrypoint for windows

## [0.5] - 2021-01-21

### Added 

- Add markdown table support

### Changed

- Improve python 3 support
- Improve Docker support

## [0.4] - 2016-10-12

### Added

- Add current directory as `base_url` to md2pdf script (Fix #6)

[unreleased]: https://github.com/jmaupetit/md2pdf/compare/3.0.1...main
[3.0.1]: https://github.com/jmaupetit/md2pdf/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/jmaupetit/md2pdf/compare/2.1.0...3.0.0
[2.1.0]: https://github.com/jmaupetit/md2pdf/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/jmaupetit/md2pdf/compare/1.0.1...2.0.0
[1.0.1]: https://github.com/jmaupetit/md2pdf/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/jmaupetit/md2pdf/compare/0.6...1.0.0
[0.6]: https://github.com/jmaupetit/md2pdf/compare/0.5...0.6
[0.5]: https://github.com/jmaupetit/md2pdf/compare/0.4...0.5
[0.4]: https://github.com/jmaupetit/md2pdf/compare/0.3...0.4
