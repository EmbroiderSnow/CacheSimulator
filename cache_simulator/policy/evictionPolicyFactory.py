from cache_simulator.policy.eviction import *

def EvictionPolicyFactory(policy_name):
    """
    Factory function to create eviction policy instances based on the policy name.

    Args:
        policy_name (str): Name of the eviction policy (e.g., 'LRU', 'FIFO').

    Returns:
        EvictionPolicy: An instance of the corresponding eviction policy class.
    """
    if policy_name == 'LRU':
        return LRU()
    elif policy_name == 'SRRIP':
        return SRRIP()
    else:
        raise ValueError(f"Unknown eviction policy: {policy_name}")