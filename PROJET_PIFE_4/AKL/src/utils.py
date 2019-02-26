import csv

order = ['TB', 'B', 'AB', 'P', 'I', 'AR']


def import_csv(ext):
    ids = []
    preferences = []

    with open('../DONNEES/preferences' + ext + '.csv') as file:
        read = csv.reader(file, delimiter=',')
        for row in read:
            if read.line_num == 1:
                ids = row[1:]
            else:
                preferences.append(row[1:])
    return ids, preferences


def write_csv(repartition):
    with open('AKL.csv', 'w') as file:
        writer = csv.writer(file, delimiter=';')
        rep = []
        for g in repartition:
            rep.append(' '.join(g))
        writer.writerow(rep)


def map_func(c, i, ids):
    if c == 'TB':
        return c, 6, ids[i]
    elif c == 'B':
        return c, 5, ids[i]
    elif c == 'AB':
        return c, 4, ids[i]
    elif c == 'P':
        return c, 3, ids[i]
    elif c == 'I':
        return c, 2, ids[i]
    elif c == 'AR':
        return c, 1, ids[i]
    else:
        return c, 7, ids[i]


def app_to_val(c):
    if c == 'TB':
        return 6
    elif c == 'B':
        return 5
    elif c == 'AB':
        return 4
    elif c == 'P':
        return 3
    elif c == 'I':
        return 2
    elif c == 'AR':
        return 1
    else:
        return 7


def sort_preferences(ids, preferences):
    temp = []
    for i, row in enumerate(preferences):
        line = []
        for j, col in enumerate(row):
            line.append(map_func(col, j, ids))
        temp.append(line)
    temp2 = []
    for row in temp:
        sorted_row = sorted(row, key=lambda tup: tup[1], reverse=True)
        temp2.append(sorted_row)
    out = []
    for i, row in enumerate(temp2):
        out.append(list(map(lambda c: c[2], row)))

    return out


def get_alone(ids, matches):
    out = []
    for id in ids:
        if not any(id in x for x in matches):
            out.append(id)
    return out


def get_group_names(groups):
    out = []
    for g in groups:
        out.append(g[0] + '_' + g[1])
    return out


def get_group_preferences(ids, preferences, group_names, alone):
    group_preferences = []
    for g in group_names:
        group = g.split('_')
        prefs = []
        for a in alone:
            pref1 = preferences[ids.index(group[0])][ids.index(a)]
            pref2 = preferences[ids.index(group[1])][ids.index(a)]
            pref = pref1 if order.index(pref1) > order.index(pref2) else pref2
            prefs.append((
                pref,
                app_to_val(pref),
                a
            )
            )
        group_preferences.append(prefs)

    temp = []
    for row in group_preferences:
        sorted_row = sorted(row, key=lambda tup: tup[1], reverse=True)
        temp.append(sorted_row)
    out = []
    for i, row in enumerate(temp):
        out.append(list(map(lambda c: c[2], row)))
    return out


def get_alone_preferences(ids, preferences, group_names, alone):
    alone_preferences = []
    for a in alone:
        prefs = []
        for name in group_names:
            group = name.split('_')
            pref1 = preferences[ids.index(a)][ids.index(group[0])]
            pref2 = preferences[ids.index(a)][ids.index(group[1])]
            pref = pref1 if order.index(pref1) > order.index(pref2) else pref2
            prefs.append((
                pref,
                app_to_val(pref),
                name
            ))
        alone_preferences.append(prefs)
    temp = []
    for row in alone_preferences:
        sorted_row = sorted(row, key=lambda tup: tup[1], reverse=True)
        temp.append(sorted_row)
    out = []
    for i, row in enumerate(temp):
        out.append(list(map(lambda c: c[2], row)))
    return out