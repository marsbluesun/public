import requests_with_caching 
import json

def get_movies_from_tastedive(keyword):
    input  = {'q': keyword, 'type': "movies", 'limit':"5"}
    output = requests_with_caching.get("https://tastedive.com/api/similar", params=input) 
    data   = json.loads(output.text)
    #print(output.text)
    return data

def extract_movie_titles(data):
    movie_title = [movie["Name"] for movie in data["Similar"]["Results"]]
    return movie_title

def get_related_titles(lst):
    print("Your input list is: {}".format(lst))
    outputlst = []
    for keyword in lst:
        extracted_lst = extract_movie_titles( get_movies_from_tastedive(keyword) )
        for movie in extracted_lst:
            if movie not in outputlst:
                outputlst.append(movie)
    return outputlst

def get_movie_data(keyword):
    input = {'t': keyword, 'r': 'json'}
    omdbapi_response = requests_with_caching.get('http://www.omdbapi.com/', params=input)
    output = json.loads(omdbapi_response.text)
    return output

def get_movie_rating(dict_OMDB):
    rotten_rating = 0
    if len(dict_OMDB['Ratings']) >1:
        if dict_OMDB['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            rotten_rating = dict_OMDB['Ratings'][1]['Value'][:2]
            rotten_rating = int(rotten_rating)
    return rotten_rating

def get_sorted_recommendations(input_list):
    related_movies = get_related_titles(input_list)
    ratings        = [get_movie_rating( get_movie_data(movie) ) for movie in related_movies ]
    movie_tuple    = sorted(zip(related_movies, ratings), key = lambda col: col[1], reverse= True)
    print("Rating tuple is : {}".format(movie_tuple))
    temp_tuple2    = movie_tuple
    sorted_list    =[]
    #output_lst     = [recommended[0] for recommended in movie_tuple]
    for i in range(len(temp_tuple2) - 1):
        if temp_tuple2[i][0] not in sorted_list:
            if temp_tuple2[i][1] == temp_tuple2[i + 1][1]:
                if temp_tuple2[i][0] < temp_tuple2[i + 1][0]:
                    sorted_list.append(temp_tuple2[i + 1][0])
                    sorted_list.append(temp_tuple2[i][0])
            else:
                sorted_list.append(temp_tuple2[i][0])
    return sorted_list
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
input_list = ["Bridesmaids", "Sherlock Holmes"]
output = get_sorted_recommendations(input_list)
#output = get_related_titles(input_list)
print("Output is : {}".format(output))