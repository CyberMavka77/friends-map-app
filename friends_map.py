import json
import twitter2
import folium
import geopy

def get_friend_location(friend_loc):
    geoloc = geopy.Nominatim(user_agent='map')
    location = geoloc.geocode(friend_loc, timeout=None)

    if location:
        return location.latitude, location.longitude
    return None

def get_followings_data(twitter_acc):
    """
    Returns data for a particular twitter account
    """
    ret_dict = dict()
    try:
        with open("twitter2.json", "w") as file:
            json.dump(twitter2.data_return(twitter_acc), file, ensure_ascii=False, indent = 4)
        with open("twitter2.json", "r") as file1:
            user_data = json.load(file1)['users']
        
        for friend in user_data:
            if friend["location"]:
                if friend["location"] in ret_dict:
                    ret_dict[friend["location"]][1].append(friend["name"])
                else:
                    friend_loc = get_friend_location(friend["location"])
                    if friend_loc:
                        ret_dict[friend["location"]] = (friend_loc,[friend["name"]])
                    else:
                        continue
            else:
                continue
        return ret_dict
    except Exception:
        return None

def create_friends_map(friends_dict):
    friends_m = folium.Map(list(friends_dict.values())[0][0], zoom_start=3)
    fg_friends = folium.FeatureGroup(name = "Friends locations")
    
    for adrr in friends_dict:
        marker_str = '\n'.join(friends_dict[adrr][1])
        fg_friends.add_child(folium.Marker(location=friends_dict[adrr][0], popup=folium.Popup(marker_str),
        icon=folium.Icon(color='purple')))
    
    friends_m.add_child(fg_friends)
    friends_m.add_child(folium.LayerControl())
    friends_m.save('templates/friends.html')

# if __name__=="__main__":
#     create_friends_map(get_followings_data("redn1njaa"))