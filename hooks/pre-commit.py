import subprocess
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_scanner import scan_file, load_patterns, load_config

# Get files staged for commit
def get_staged_files():
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip().split('\n')

# Format and display messages
def print_findings(findings):
    for issue in findings['block']:
        print("\n❌ Commit blocked: {}".format(issue['reason']))
        print("🔒 File: {}:{} → {}".format(issue['file'], issue['line'], issue['content']))
        if 'Sensitive' in issue['reason']:
            print("\nSecrets like passwords, tokens or API keys should never be hardcoded.")
            print("Please move them to environment variables or a secure vault.")
        elif 'production' in issue['reason']:
            print("\nMake sure production settings do not expose debug information or allow wildcard hosts.")

    for issue in findings['warn']:
        print("\n⚠️ Warning: {}".format(issue['reason']))
        print("📄 File: {}:{} → {}".format(issue['file'], issue['line'], issue['content']))
        print("This is allowed in staging but will be blocked in production.")

# Main hook function
def main():
    config = load_config()
    env = config.get('env', 'dev')
    print(f"🔍 Running commit-guardian in environment: {env}\n")

    patterns_by_env = load_patterns()
    staged_files = get_staged_files()

    total_findings = {'block': [], 'warn': []}

    for file in staged_files:
        if not file.endswith(('.py', '.js', '.ts', '.env', '.json')):
            continue
        result = scan_file(file, patterns_by_env, env)
        total_findings['block'].extend(result['block'])
        total_findings['warn'].extend(result['warn'])

    if total_findings['block']:
        print_findings(total_findings)
        sys.exit(1)

    if total_findings['warn']:
        print_findings(total_findings)

    print("✅ No critical issues found. Commit allowed.")

if __name__ == '__main__':
    main()
    exit(0)
