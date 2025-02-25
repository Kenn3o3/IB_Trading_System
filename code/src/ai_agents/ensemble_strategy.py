def ensemble_decision(trader_decisions):
    votes = {"buy": 0, "sell": 0, "hold": 0}
    for decision in trader_decisions:
        votes[decision] += 1
    return max(votes, key=votes.get)