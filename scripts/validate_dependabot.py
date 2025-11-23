import yaml
import json
import jsonschema
import sys
from pathlib import Path

def validate_dependabot_config(config_path, schema_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        with open(schema_path, 'r') as f:
            schema = json.load(f)
            
        jsonschema.validate(instance=config, schema=schema)
        print(f"✅ Configuration at {config_path} is valid.")
        return 0
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ Validation Error: {e.message}")
        print(f"Path: {' -> '.join(str(p) for p in e.path)}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    config_file = base_dir / ".github" / "dependabot.yml"
    schema_file = base_dir / "scripts" / "dependabot-schema.json"
    
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)
        
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        sys.exit(1)
        
    sys.exit(validate_dependabot_config(config_file, schema_file))
