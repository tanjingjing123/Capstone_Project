"""
# Usage
import music_recommendation_lib

# list of music information tuple
# Each element will be (MUSIC_NAME, AUTHOR, YOUTUBE_LINK)
print(music_recommendation_lib.GetRecommendation('happy'))
"""
import collections


def load_music_list():
    music_database = collections.defaultdict(list)
    music_labels = collections.defaultdict(list)
    with open('musics') as music_file:
        music_type = ''
        labels = []
        for line in music_file:
            line = line.strip()
            if not line:
                for label in labels:
                    music_labels[label] += music_database[music_type]
                labels = []
                continue
            if '+' in line:
                labels.append(line.replace('+', '').strip().lower())
            elif '~' in line:
                line = line.replace('~', '')
                arr = line.split('|')
                music_database[music_type].append((arr[0].lower().strip(), arr[1].strip(), arr[2].strip()))
            else:
                music_type = line.lower()
    return music_database, music_labels


def hamming_distance(string1, string2):
    distance = 0
    l = min(len(string1), len(string2))
    for i in range(l):
        if string1[i] != string2[i]:
            distance += 1
    return distance


def recommend(string, music_database, music_labels):
    string = string.lower()
    if string in music_labels:
        return music_labels[string]
    if string in music_database:
        return music_database[string]
    result = []
    for arr in music_database.values():
        for song, author, link in arr:
            if string in song or string in author.lower():
                result.append((song, author, link))
    if result:
        return result
    min_distance = -1
    best_category = None
    for category in music_database.keys():
        distance = hamming_distance(string, category)
        if min_distance == -1 or distance < min_distance:
            min_distance = distance
            best_category = category
    return music_database[best_category]


def GetRecommendation(keyword):
    music_list, music_by_labels = load_music_list()
    return recommend(keyword, music_list, music_by_labels)
