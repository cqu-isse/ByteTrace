"""Optional maintainer smoke check (Python 3 standard library only)."""
from pathlib import Path
import os
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
java_home = os.environ.get("JAVA_HOME")
def executable(name):
    return str(Path(java_home) / "bin" / name) if java_home else name

def run(command, cwd):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr

with tempfile.TemporaryDirectory(prefix="bytetrace-check-") as directory:
    work = Path(directory)
    run([executable("javac"), "-g", "-source", "8", "-target", "8", "-d", str(work),
         str(root / "examples/simple-java/Example.java")], work)
    for value, expected in [(3, 8), (-3, 0)]:
        config = work / "trace.properties"
        trace = work / (str(value) + ".log")
        original = work / (str(value) + "-original.log")
        config.write_text("args.use.specified=true\nargs.methods=Example::calculate,Example::doubleValue\n"
                          + "log.file.path=" + trace.name + "\nori.log.file.path=" + original.name + "\n", encoding="utf-8")
        baseline = run([executable("java"), "-cp", str(work), "Example", str(value)], work)
        output = run([executable("java"), "-javaagent:" + str(root / "build/libs/ByteTrace.jar") + "=" + config.name,
                      "-cp", str(work), "Example", str(value)], work)
        assert baseline.strip() == "RESULT=" + str(expected), baseline
        assert baseline.strip() in output.splitlines(), output
        assert trace.exists(), output
        events = trace.read_text()
        assert "[Local Variables]" in events and "[Control Flow]" in events, events
        assert ('Executed: true' if value == 3 else 'Executed: false') in events, events
        if value == 3:
            assert "[Method Call]" in events and "Example.doubleValue" in events, events
        else:
            assert "[Method Call]" not in events, events
        assert "[Local Variables]" in original.read_text()
        assert "defects4j.build.properties" not in output
        print("PASS input=" + str(value) + " result=" + str(expected) + ": behavior and trace events verified")
