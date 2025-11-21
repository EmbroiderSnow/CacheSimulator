from cache_simulator.policy.bypass import *

def BypassPolicyFactory(config):
    if config == None:
        return NoBypass()
    policy_name = config.get("policy_name", "NoBypass")
    if policy_name == "NoBypass":
        return NoBypass()
    elif policy_name == "Prob":
        return ProbBypass(config.get("bypass_prob_demand", 0.05), config.get("bypass_prob_prefetch", 0.2))
    else:
        return NoBypass()