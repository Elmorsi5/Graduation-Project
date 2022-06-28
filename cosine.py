def cosine_sim(file, utag):
    import numpy as np
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import json

    dic = {}
    ndata = json.loads(file)
    for x in ndata:
        df = pd.DataFrame.from_dict(ndata[x])
        df.set_index('id')
        features = ['labels']
        for feature in features:
            df[feature] = df[feature].fillna('')
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df["labels"])
        cosine_sim = cosine_similarity(count_matrix)

        user_tag = utag

        def get_index_from_title(tag):
            return df[df.labels == user_tag]["id"].values[0]

        case_index = get_index_from_title(user_tag)
        similar_cases = list(enumerate(cosine_sim[case_index]))
        sorted_similar_cases = sorted(similar_cases, key=lambda x: x[1], reverse=True)

        def get_title_from_index(index):
            return df[df.id == index]["id"].values[0]

        i = 0
        l = []
        for case in sorted_similar_cases:
            l.append(get_title_from_index(case[0]))
            i = i + 1
            if i > 15:
                break
        dic[x] = l
    return dic
