"""List configured Hermes model candidates, with Magpie routes first."""

import argparse
import json
import subprocess


def model_ids(settings):
    catalog = settings.get('models')
    if isinstance(catalog, dict):
        return [name for name in catalog if isinstance(name, str) and name]
    if not isinstance(catalog, list):
        return []
    result = []
    for entry in catalog:
        if isinstance(entry, dict):
            entry = entry.get('id') or entry.get('model') or entry.get('name')
        if isinstance(entry, str) and entry and entry not in result:
            result.append(entry)
    return result


def discover(providers, active_model):
    if isinstance(active_model, str):
        active_model = {'default': active_model}
    active_provider = active_model.get('provider')
    active_id = active_model.get('default')
    configured = dict(providers)
    if isinstance(active_provider, str) and active_provider not in ('', 'auto'):
        configured.setdefault(active_provider, {})

    def priority(name):
        if name == 'magpie':
            return 0
        if name.startswith('magpie-'):
            return 1
        return 2 if name == active_provider else 3

    routes = []
    for name in sorted(configured, key=priority):
        settings = configured[name]
        if not isinstance(settings, dict) or settings.get('enabled') is False:
            continue
        models = model_ids(settings)
        default = active_id if name == active_provider and isinstance(active_id, str) else None
        routes.append({'provider': name, 'active_model': default, 'catalog_models': models})
    return routes


def read_setting(command, key, default):
    result = subprocess.run(
        [*command, 'config', 'get', key, '--json'],
        capture_output=True, encoding='utf-8', timeout=15,
    )
    if result.returncode:
        missing = f'Config key not set: {key}'
        if missing in (result.stderr + result.stdout).splitlines():
            return default
        raise ValueError(f'Hermes could not read the {key} setting')
    try:
        return json.loads(result.stdout)
    except ValueError:
        raise ValueError(f'Hermes did not return JSON for {key}') from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', help='Read a named Hermes profile')
    arguments = parser.parse_args()
    command = ['hermes', '-p', arguments.profile] if arguments.profile else ['hermes']
    try:
        providers = read_setting(command, 'providers', {})
        model = read_setting(command, 'model', {})
        if not isinstance(providers, dict) or not isinstance(model, (dict, str)):
            raise ValueError('Unexpected shape for Hermes provider or model settings')
        routes = discover(providers, model)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f'Model discovery failed: {error}\n')
    print(json.dumps({'source': 'configuration', 'routes': routes}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
