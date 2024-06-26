import os
import yaml
import roam.config


def load(path):
    try:
        with open(path, 'r') as f:
            settings = yaml.safe_load(f)
            if settings is None:
                settings = {}
            return settings
    except IOError:
        return {}


def syncprovders():
    from roam.syncing import replication
    path = os.path.dirname(roam.config.loaded_path)
    settings = load(os.path.join(path, 'sync.config'))
    providers = settings.get("providers", {})
    variables = {}
    for name, config in providers.items():
        if name == "variables":
            variables.update(config)
            continue

        cmd = config['cmd']
        cmd = os.path.join(path, cmd)
        synctype = config.get('type', "replication")
        if synctype in ['replication', 'batch']:
            config['cmd'] = cmd
            config['rootfolder'] = path
            config.setdefault('variables', variables)
            config.update(variables)
            yield replication.BatchFileSync(name, None, **config)
