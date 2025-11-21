from cache_simulator.policy.prefetch import *

def PrefetchPolicyFactory(config):
    if config is None:
        return NoPrefetch()
    policy_name = config.get('policy_name', None)
    if policy_name == 'NextNLine':
        return NexNLine(degree=config.get('degree', 1))
    elif policy_name == 'Stream':
        return Stream(degree=config.get('degree', 4), table_size=config.get('table_size', 8))
    elif policy_name == 'Stride':
        return Stride(degree=config.get("degree", 4), table_size=config.get("table_size", 8))
    elif policy_name == 'None' or policy_name is None:
        return NoPrefetch()
    else:
        print(f"Warning: Unknown prefetch policy '{policy_name}', using NoPrefetch.")
        return NoPrefetch()