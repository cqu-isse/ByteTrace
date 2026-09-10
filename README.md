# ByteTrace

ByteTrace is the Java bytecode instrumentation agent used by [DynaFix](https://github.com/gujiprogram/DynaFix). It records local-variable states, branch/loop events, and method-call events for explicitly selected methods. This repository contains the independent source, Gradle build, and a standalone Java example. Running the agent does not require DynaFix, Python, an LLM, or an API key.

## Build from source

Install a JDK and set `JAVA_HOME` to its installation directory. The included Gradle 8.4 wrapper runs on JDK 8 through 20; JDK 11 is recommended for this release. The build requests a **JDK 8 toolchain** and can download it through the configured Foojay resolver. The first build needs network access to Gradle, Maven Central, the plugin portal, and the toolchain provider. No separate Gradle or Kotlin installation is required.

```bash
git clone https://github.com/gujiprogram/ByteTrace.git
cd ByteTrace
chmod +x gradlew
./gradlew clean build
```

On Windows PowerShell, use `./gradlew.bat clean build` instead. The self-contained agent is generated at **`build/libs/ByteTrace.jar`**. Use this fat JAR, not the plain project JAR. The manifest declares `Premain-Class: anonymous.DetectAgent`.

Prebuilt binaries are available from [Releases](https://github.com/gujiprogram/ByteTrace/releases). Download `ByteTrace.jar` and check it against the accompanying `SHA256SUMS` file. The source tag and release JAR belong to the same version.

## Run the standalone example

Run all commands from the repository root after building:

```bash
javac -g -d examples/simple-java/classes examples/simple-java/Example.java
java "-javaagent:build/libs/ByteTrace.jar=examples/simple-java/bytetrace.properties" -cp examples/simple-java/classes Example
```

These commands also work in PowerShell. When using a downloaded JAR, replace `build/libs/ByteTrace.jar` with its path. The example should print `RESULT=8` (alongside instrumentation diagnostics) and create:

- `examples/simple-java/trace.log`: compact variable-state and control-flow/method-call events.
- `examples/simple-java/trace-original.log`: variable observations before compact-log filtering.

The current logger rotates each file at 5 KB; also inspect the `.1` backup. These are bounded diagnostic traces, not an unlimited execution archive. Delete old example logs before comparing repeated runs because appenders append to existing files.

## Trace your own application

Compile target classes with debugging metadata (`javac -g`), create a properties file, and attach the agent when starting the JVM:

```properties
args.use.specified=true
args.methods=com.example.Calculator::calculate,com.example.Calculator::helper
log.file.path=trace.log
ori.log.file.path=trace-original.log
changedLocalVarsOnly=false
```

```bash
java "-javaagent:/absolute/path/ByteTrace.jar=/absolute/path/bytetrace.properties" -cp /path/to/classes com.example.Main
# Or for an executable application JAR:
java "-javaagent:/absolute/path/ByteTrace.jar=/absolute/path/bytetrace.properties" -jar application.jar
```

The agent argument is a **properties-file path**, not an inline list of options. Select methods by fully qualified class name, `::`, and method name, separated by commas without spaces. Overloads share the same name selector; descriptor-level selection is not implemented. Make output directories beforehand. Relative output paths resolve against the target JVM's working directory. Use UTF-8 for the properties file. In Windows properties files use forward slashes, e.g. `C:/work/trace.log`. On Windows JDK 8/11, prefer a relative ASCII-only properties filename after `=`: non-ASCII characters in the JVM agent argument can be misdecoded.

| Property | Default | Meaning |
| --- | --- | --- |
| `args.use.specified` | `false` | Set `true` for the explicit method selectors shown above. |
| `args.methods` | empty | Comma-separated `fully.qualified.Class::method` selectors. Required for the documented standalone workflow. |
| `log.file.path` | `bugDetect.log` | Compact trace output. |
| `ori.log.file.path` | `bugDetectOri.log` | Original variable-observation output. |
| `changedLocalVarsOnly` | `false` | Limit inserted variable observations to first visits and recognized local-variable writes. |

`args.classes` is a legacy configuration field; it does not select every method in a class. Use explicit `args.methods`. Defects4J metadata loading remains for compatibility, but it is not required for this standalone workflow.

## Output and limitations

Events contain the class, method, a source-line marker, and one of `[Local Variables]`, `[Control Flow]`, or `[Method Call]`. Variable payloads are JSON; other events are text. `[Method Call]` records a caller/callee event, not a complete stack snapshot. Branch conditions are reconstructed from bytecode and may be approximate. Local-variable reporting depends on debug metadata; variable markers retain the original implementation's line-offset convention.

The compact log suppresses repeated values and large serialized values. It is intended for debugging context, not a lossless or per-thread execution record. The agent retains the original diagnostic console output. Start with a small set of methods; custom class loaders, constructors, concurrent programs, and newer bytecode require application-specific validation. Check both program behavior and trace contents before applying the tool to a new project.

## Verification

`python scripts/verify_example.py` is an optional maintainer check (Python 3, standard library only). It compiles the fixture with debug metadata, compares instrumented and uninstrumented results for both branches, and checks variable, branch, and method-call events. Python is not needed for normal agent use. GitHub Actions runs this check after building.

## DynaFix / Defects4J integration

See [docs/defects4j.md](docs/defects4j.md). The DynaFix repository maintains benchmark checkout, failing-test execution, trace post-processing, and repair iteration. ByteTrace provides the agent JAR. Download a fixed ByteTrace release and configure DynaFix's `ant_debug` script to use that JAR.

## Provenance and citation

Extracted from `ByteTrace/ByteTrace_code` in [DynaFix commit a8f0add](https://github.com/gujiprogram/DynaFix/commit/a8f0add2305a405276bf100d51536e05785aecdf), with the source-directory history retained. The independent release includes packaging/documentation changes and permits the absence of Defects4J metadata for ordinary Java programs. See [CHANGELOG.md](CHANGELOG.md) for release changes and validation.

If you use ByteTrace in research, please cite the DynaFix paper:

```bibtex
@article{huang2025dynafix,
  title={DynaFix: Iterative Automated Program Repair Driven by Execution-Level Dynamic Information},
  author={Huang, Zhili and Xu, Ling and Liu, Chao and Sun, Weifeng and Zhang, Xu and Lei, Yan and Yan, Meng and Zhang, Hongyu},
  journal={arXiv preprint arXiv:2512.24635},
  year={2025}
}
```

## Third-party notices

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Original third-party source headers are retained. No new project-wide license is granted by this extraction; the source repository did not include one.
