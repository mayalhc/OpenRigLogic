# Contributing to OpenRigLogic

OpenRigLogic is an open source project maintained by Epic Games, and we welcome contributions from anyone.

Before you begin, read our [Code of Conduct](CODE_OF_CONDUCT.md). 

## Ways to contribute

We welcome code contributions - bug fixes, features, performance improvements. There are also plenty of ways to help beyond writing code:

- **Report a bug** - open a GitHub Issue with steps to reproduce  
- **Request a feature** - open a GitHub Issue  
- **Improve documentation** - fix typos, clarify explanations, add examples  
- **Triage issues** - help reproduce bugs, add labels, confirm scope  
- **Review pull requests** - read the code, test it, leave thoughtful feedback

## Getting started

### Prerequisites

You need the following tools installed:

- C/C++ compiler  
- [CMake](https://cmake.org/documentation/)  
- [Google Test](https://github.com/google/googletest) and [Google Benchmark](https://github.com/google/benchmark) \- required for unit tests and benchmarks.  These are acquired automatically through a cmake helper module and do not need to be installed separately.

### Build and test

OpenRigLogic uses CMake to generate build scripts. From the repository root:

```
mkdir build
cd build
cmake ..
```

To build:

```
cmake --build .

```

Tests can be run through CMake. When the active build system is MSBuild, the build configuration must be supplied on the command line:

```
ctest -C Debug
ctest -C Release

```

For make and ninja, only one build configuration is active at a time, so:

```shell
ctest
```

## Before you code

For anything beyond a trivial fix (such as documentation or tests), **open a GitHub Issue before writing code**.

OpenRigLogic is highly optimised for realtime performance on a wide range of platforms (including console and mobile devices).  Realtime performance and platform independence is a critical design feature.

Changes will not be accepted if they;

- Work only with a subset of MetaHuman characters;   
- Break compatibility with previously-released MetaHuman characters;   
- Compromise compatibility with the broader MetaHuman ecosystem, including Unreal Engine;   
- Are already being addressed by another issue or pull request;  
- Are intentionally out of scope.

Discussing the proposed change in an issue gives a maintainer the opportunity to weigh in before investing significant effort.

## Development workflow

### Branching

OpenRigLogic uses the following branching strategy:

- **`main`** corresponds to the active development branch for the next release. **All contributions target `main`.**  
- **Stable branches** (for example `5.8`) are immutable snapshots aligned with specific Unreal Engine releases. We do not accept changes against stable branches, and we do not backport accepted changes from `main` to older versions. 

Fork the repository to your own GitHub account, then create a feature branch from `main`:

```shell
git checkout -b feature/short-description main
```

### Formatting and linting

A `.clang-format` file is included in the repository and should be recognised by most modern IDEs.  These formatting rules are enforced by CI and must pass before any PR is merged. Python bindings should be consistent with the surrounding code.

### Commit messages

Write commit messages in the imperative: "Add NEON path for RigLogic evaluation on ARM64", not "Add NEON path". Keep the subject line under 72 characters. Include a body when the why isn't obvious from the subject alone.

Reference the issue your change addresses:

```
Add NEON path for RigLogic evaluation on ARM64

RigLogic evaluation on ARM64 previously fell back to scalar code.
This commit adds a NEON intrinsics path matching the performance
characteristics of the existing x86 SSE path.

The implementation is gated behind PLATFORM_ENABLE_VECTORINTRINSICS_NEON
and falls back to scalar code on platforms where intrinsics are unavailable.

Fixes #123
```

### DCO sign-off

Every commit must include a `Signed-off-by:` line. This certifies that your contribution complies with the [Developer Certificate of Origin](DCO) (DCO) - a lightweight declaration that you have the right to submit the change under the MIT license.

Add the sign-off automatically with:

```
git commit -s -m "Your commit message"
```

This appends:

```
Signed-off-by: Your Name you@example.com
```

Commits without a sign-off will not be merged.

Because the MIT license doesn't include an express patent grant, the DCO sign-off also carries an affirmation about patents. By signing off on your commit, you affirm that, to the best of your knowledge, your contribution doesn't infringe any patents you are aware of. Providing your sign-off is a representation about your knowledge, not a grant of any patent license. 

## Submitting a pull request

1. Fork the repository.  
2. Make your changes and ensure all tests pass and linting is clean.  
3. Add or update tests for the behavior you're changing.  
4. Open a pull request targeting `main`. The PR description should cover:  
- **What:** what does this PR do?  
- **Why:** what problem does it solve? Link to the GitHub Issue.  
- **How:** a brief description of your approach, especially if non-obvious.  
- **Testing:** how did you verify the change works?  
5. Every commit must include `Signed-off-by:` as described above.

Keep PRs focused. One logical change per PR. 

If your change touches RigLogic's evaluation hot path, include a short performance impact note in the pull request description. Where applicable, provide before-and-after measurements on a representative platform.

## Review process

Expect at least one round of feedback before a PR is merged.

Address each piece of feedback, then re-request review. Maintainer decisions are final. If feedback isn't clear, ask. 

As part of the review process, the contribution will be run through a broader test suite.  The CI that runs on GitHub is a small subset of the test matrix required to guarantee performance and platform independence. Reviewers may surface failures from the wider matrix during the review conversation and ask you to address them.

In rare cases where iteration becomes impractical \- typically when a platform-specific issue is hard to reproduce externally \- a reviewer may complete the final stretch of a change themselves. When a reviewer completes a change, a contributor's original commits remain attributed to that contributor.

## Proposing a feature

Use the **Feature Proposal** issue template. A good proposal includes:

1. **Problem statement** \- What problem does this solve? Who benefits?  
2. **Proposed solution** \- How would you approach it? Be as specific as you can.  
3. **Alternatives considered** \- What other approaches did you think about?  
4. **Scope** \- Is this a small utility or a large architectural change?  
5. **Engine and platform compatibility** \- Does this depend on a specific Unreal Engine version or API? Will it work across all platforms RigLogic supports? Will it work for all MetaHuman characters, or only a subset?

## Documentation

Documentation changes follow the same PR process as code. 

## Community

Get help by opening a GitHub Issue or bring the conversation to the [MetaHuman category of the Unreal Engine forums](https://forums.unrealengine.com/categories?tag=metahuman).

Issues tagged [`good first issue`](https://github.com/EpicGames/OpenRigLogic/labels/good%20first%20issue) are a good starting point if you're new to the codebase. 

### AI assistance policy

Contributions that used AI tools (GitHub Copilot, Claude, etc.) are welcome. When you do, you must:

- **Disclose** which AI tools you used in the PR description.  
- **Review and test** all AI-generated code. You remain fully responsible for its correctness, security, and license compliance.  
- **Write your own PR description** - AI-generated PR descriptions are not accepted.

For security-sensitive changes (cryptography, authentication, authorization), disclose AI involvement early and expect closer review. 

## Legal

### License

OpenRigLogic is licensed under the [MIT License](LICENSE). By submitting a pull request, you agree that your contribution may be used under that license.

All commits must include a `Signed-off-by:` line as described in the [DCO sign-off](#dco-sign-off) section. This confirms your agreement with the [Developer Certificate of Origin](DCO). 

### Copyright headers

Preserve your own copyright on the code you contribute. For new files, add a copyright line and an SPDX identifier at the top:

```
// Copyright 2026 Jane Smith 
// SPDX-License-Identifier: MIT
```

When modifying existing files, leave Epic's copyright line in place and add your own below it. 

### License compatibility

Contributed code must not introduce dependencies licensed under the GPL, LGPL, or AGPL. Their copyleft terms are incompatible with OpenRigLogic's MIT license.  
