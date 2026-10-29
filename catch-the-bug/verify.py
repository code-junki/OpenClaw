import ast
import base64
import subprocess
import sys

# The completion code is only decoded and shown when every check passes.
_CODE = "QU1ELUFBSTI2LVBBTkVMLTlLNFE="

MODULE = "typing_stats.py"


def structural_findings(path):
    """Return the perf/readability issues that are still unresolved.

    These mirror what the performance and readability reviewers report. The
    Fixer must apply their findings for this list to come back empty, so a
    green run means the whole panel (reviewers + Fixer) did its job, not just
    that the behavior bugs happened to get patched.
    """
    tree = ast.parse(open(path).read())
    issues = []

    # Readability: unused `import math`
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(a.name == "math" for a in node.names):
            issues.append("readability: remove the unused `import math`")
            break

    # Readability: unused module-level `BONUS`
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "BONUS":
                    issues.append("readability: remove the unused `BONUS` global")

    # Performance: O(n^2) string-building loop inside summarize
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "summarize":
            if any(isinstance(n, ast.For) for n in ast.walk(node)):
                issues.append(
                    "performance: remove the O(n^2) string-building loop in summarize"
                )

    return issues


def main():
    line = "=" * 52

    # Gate 1 - behavior. The bugs must be fixed so the tests pass.
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"])
    print()
    if result.returncode != 0:
        print("Behavior checks failed. Fix the bugs above,")
        print("then re-run:  python verify.py")
        sys.exit(1)

    # Gate 2 - the panel's findings must actually be applied by the Fixer.
    issues = structural_findings(MODULE)
    if issues:
        print("Behavior checks passed, but the panel's findings")
        print("are not all resolved yet:")
        for issue in issues:
            print("  - " + issue)
        print()
        print("Have your Fixer apply the panel's review,")
        print("then re-run:  python verify.py")
        sys.exit(1)

    code = base64.b64decode(_CODE).decode()
    print(line)
    print("  ALL CHECKS PASSED")
    print("  Completion code: " + code)
    print("  Show this code AND your panel's review output")
    print("  (the issues it flagged) to a workshop host")
    print("  to claim your gift.")
    print(line)
    sys.exit(0)


if __name__ == "__main__":
    main()
