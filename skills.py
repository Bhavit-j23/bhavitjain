def extract_skills(text):

    skill_list = open("skills.txt").read().splitlines()

    found = []

    text = text.lower()

    for s in skill_list:

        if s in text:
            found.append(s)

    return found