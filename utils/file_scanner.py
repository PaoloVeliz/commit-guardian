import re
import yaml
import json

# Load environment configuration from JSON
def load_config(path='config/default.json'):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return {"env": "dev"}  # Default

# Load patterns from YAML
def load_patterns(path='rules/patterns.yaml'):
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        print(f"error while reading pattern file {e}")
        return {}

# Scan a file using the appropriate patterns
def scan_file(filepath, patterns_by_env, current_env):
    findings = {
        'block': [],
        'warn': []
    }
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return findings
    # Universal rules that always block commits
    for i, line in enumerate(lines, 1):
        for pattern in patterns_by_env.get('secrets', []):
            if re.search(pattern, line):
                findings['block'].append({
                    'file': filepath,
                    'line': i,
                    'content': line.strip(),
                    'reason': 'Sensitive information detected'
                })

    # Environment-specific rules
    if current_env == 'staging':
        for i, line in enumerate(lines, 1):
            for pattern in patterns_by_env.get('staging_block', []):
                if re.search(pattern, line):
                    findings['warn'].append({
                        'file': filepath,
                        'line': i,
                        'content': line.strip(),
                        'reason': 'Debug log detected (will block in production)'
                    })

    if current_env == 'prod':
        for i, line in enumerate(lines, 1):
            for pattern in patterns_by_env.get('staging_block', []) + patterns_by_env.get('prod_block', []):
                if re.search(pattern, line):
                    findings['block'].append({
                        'file': filepath,
                        'line': i,
                        'content': line.strip(),
                        'reason': 'Insecure code/config for production'
                    })

    return findings
