def fuzzy_score(skill_count, exp):

    if skill_count >= 5 and exp >= 3:
        return 90

    elif skill_count >= 3:
        return 70

    elif skill_count >= 1:
        return 50

    else:
        return 30