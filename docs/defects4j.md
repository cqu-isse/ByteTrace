# Use ByteTrace with DynaFix and Defects4J

DynaFix's Python scripts generate `temp.properties`, select methods, run failing tests, and process the logs. They remain in [DynaFix](https://github.com/gujiprogram/DynaFix). Install its Python and Defects4J dependencies following that repository's README.

1. Download `ByteTrace.jar` from a fixed [release](https://github.com/gujiprogram/ByteTrace/releases/tag/v1.0.0), or build it from the matching source tag.
2. In `{Defects4J_HOME}/major/bin/`, create an executable `ant_debug` script using the following template. Replace `/absolute/path/ByteTrace.jar`.

```bash
#!/usr/bin/env bash
BASE="$(dirname "$0")/.."
if [ -z "$JAVA_HOME" ]; then
    CMD="java"
else
    CMD="$JAVA_HOME/bin/java"
fi
TEMP_PROPERTIES=${TEMP_PROPERTIES:-./temp.properties}
exec "$CMD" \
    "-javaagent:/absolute/path/ByteTrace.jar=$TEMP_PROPERTIES" -Xverify:none \
    -XX:ReservedCodeCacheSize=256M \
    -Djava.awt.headless=true \
    "-Xbootclasspath/a:$BASE/config/config.jar" \
    -jar "$BASE/lib/ant/ant-launcher.jar" "$@"
```

```bash
chmod +x "${Defects4J_HOME}/major/bin/ant_debug"
```

3. Set DynaFix's checkout, input/output, and `major_root` paths. Its adapter sets `TEMP_PROPERTIES` for the target JVM. The generated configuration uses `args.use.specified=true`, `args.methods`, `log.file.path`, and `ori.log.file.path`, which are preserved by ByteTrace.
4. Run the DynaFix workflow as documented there. The adapter temporarily replaces the Major `ant` launcher and restores it afterward. Use an isolated Major installation per concurrently executing repair process.

The `-Xverify:none` flag above is retained from the original DynaFix integration. The standalone example is tested without disabling bytecode verification. Defects4J/Ant child-JVM behavior is project-specific; verify actual `[Local Variables]`, `[Control Flow]`, and `[Method Call]` events rather than treating console output or an existing log file as proof of instrumentation.

This extraction does not repair or revalidate DynaFix's Python orchestration. In particular, the legacy batch collection entry point has argument/import mismatches and requires a separate fix before it can serve as a standalone batch command. Use the independent Java example in this repository to verify the agent itself.
