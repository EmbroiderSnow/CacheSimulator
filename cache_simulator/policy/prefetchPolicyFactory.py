from cache_simulator.policy.prefetch import *

def PrefetchPolicyFactory(policy_name, degree=1):
    if policy_name == 'NextNLine':
        return NexNLine(degree=degree)
    elif policy_name == 'None' or policy_name is None:
        return NoPrefetch()
    else:
        print(f"Warning: Unknown prefetch policy '{policy_name}', using NoPrefetch.")
        return NoPrefetch()