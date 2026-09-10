# Changelog

## 1.0.0 ? independent repository

- Extracted the ByteTrace source-directory history from DynaFix commit `a8f0add2305a405276bf100d51536e05785aecdf`.
- Moved the existing Gradle project to the repository root; removed tracked IDE settings.
- Named the Gradle project ByteTrace and versioned the distribution as 1.0.0.
- Allow missing Defects4J metadata for standalone applications; close the metadata reader after loading. Instrumentation and log semantics are otherwise retained.
- Added build/use/configuration documentation, a standalone Java fixture, Defects4J integration notes, third-party notices, and a CI smoke check.

### Local validation

- Clean Gradle 8.4 build on Windows with JDK 11.0.18 and the JDK 8 compilation toolchain: passed.
- Standalone smoke check on JDK 11.0.18 and JDK 8u341: passed for inputs 3 and -3. Program results match the uninstrumented baseline; variable and both branch-outcome events are present; method-call events appear only on the calling branch.
- Bytecode verification remained enabled for the standalone checks.
- No end-to-end Defects4J repair experiment was run for this extraction. Linux CI results are reported separately by GitHub Actions.

The prebuilt JAR is compiled from this release's source. It is not claimed to be byte-for-byte identical to the legacy JAR formerly stored in DynaFix.
