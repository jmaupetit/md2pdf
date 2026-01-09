# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[unreleased]: https://github.com/jmaupetit/md2pdf/compare/1.0.1...main
[1.0.1]: https://github.com/jmaupetit/md2pdf/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/jmaupetit/md2pdf/compare/0.6...1.0.0
[0.6]: https://github.com/jmaupetit/md2pdf/compare/0.5...0.6
[0.5]: https://github.com/jmaupetit/md2pdf/compare/0.4...0.5
[0.4]: https://github.com/jmaupetit/md2pdf/compare/0.3...0.4
