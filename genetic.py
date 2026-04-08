def rank_candidates(data):

    ranked = sorted(data,
                    key=lambda x: x[1],
                    reverse=True)

    return ranked