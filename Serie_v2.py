import datetime
from imdbpie import Imdb
#from mechanize import Browser
#from getpass import getpass
imdb = Imdb()
"""
br=Browser()
br.set_handle_robots(False)
br.open("https://www.yggtorrent.is/user/login")
br.select_form(nr=1)
br["id"]=getpass("Rentrer votre identifiant: \n")
br["pass"]=getpass("Rentrer votre mot de passe :\n")
br.submit()
"""

class Serie:
    def __init__(self, name,tag,season,episode):
        self._name = name
        self._tag = tag
        self._season = season
        self._current_episode = episode
        self._end = False
        request = imdb.get_title_episodes_detailed(self._tag,self._season)
        self._last_update = datetime.datetime.now()
        self._nb_episodes = request["totalEpisodes"]
        if self._nb_episodes < self._current_episode:
            self._current_episode = 1
        self._nb_seasons = len(imdb.get_title_episodes(self._tag)["seasons"])
        self._current_ep_data = [request["episodes"][self._current_episode - 1]["episodeNumber"],request["episodes"][self._current_episode-1]["releaseDate"]["first"]["date"]]
        self._remaining_ep_data = []
        for i in range(self._nb_episodes):
            if i > self._current_episode-1:
                self._remaining_ep_data.append([request["episodes"][i]["episodeNumber"],request["episodes"][i]["releaseDate"]["first"]["date"]])

    def _get_name(self):
        return self._name
    def _set_name(self, n):
        self._name = n
    def _get_tag(self):
        return self._tag
    def _set_tag(self, t):
        self._tag = t
    def _get_season(self):
        return self._season
    def _set_season(self,s):
        self._season = s
    def _get_end(self):
        return self._end
    def _set_end(self, e):
        self._end = e
    def _get_last_update(self):
        return self._last_update
    def _set_last_update(self,d):
        self._last_update = d
    def _get_current_episode(self):
        return self._current_episode
    def _set_current_episode(self,ep):
        self._current_episode = ep
    def _get_episode_date(self):
        return self._current_ep_data[1]
    def _get_nb_episodes(self):
        return self._nb_episodes
    def _set_nb_episodes(self,nb_ep):
        self._nb_episodes = nb_ep
    def _get_nb_seasons(self):
        return self._nb_seasons
    def _set_nb_seasons(self,nb_s):
        self._nb_seasons = nb_s
    def _get_remaining_ep_data(self):
        return self._remaining_ep_data
    def _set_remaining_ep_data(self,data):
        self._remaining_ep_data = data
    def _get_current_ep_data(self):
        return self._current_ep_data
    def _set_current_ep_data(self,data):
        self._current_ep_data = data

    def update_data(self):
        request = imdb.get_title_episodes_detailed(self._tag,self._season)
        self._current_ep_data = [request["episodes"][self._current_episode - 1]["episodeNumber"],request["episodes"][self._current_episode-1]["releaseDate"]["first"]["date"]]
        self._remaining_ep_data = []
        for i in range(self._nb_episodes):
            if i > self._current_episode-1:
                self._remaining_ep_data.append([request["episodes"][i]["episodeNumber"],request["episodes"][i]["releaseDate"]["first"]["date"]])
        self._last_update = datetime.datetime.now()
        with open("MaJ","ab") as MaJ:
            MaJ.write(self._name + ": Last Update -> "+ str(self._last_update) + "\n")


    def show(self):
        #print(self._name)
        if self.is_out() :
            date = "Sorti "#(" + self._get_episode_date() + ")"
        else:
            date = self._get_episode_date()
            if date == None:
                date = "Inconnu"
        if (self._current_episode<10):
            #print("S0"+str(self._season)+"E0"+str(self._current_episode)+": "+ date)
            return "S0"+str(self._season)+"E0"+str(self._current_episode)+": "+ date
        else:
            #print("S0"+str(self._season)+"E"+str(self._current_episode)+": "+ date)
            return "S0"+str(self._season)+"E"+str(self._current_episode)+": "+ date

    def is_out(self):
        ep_date = self._get_episode_date()
        if ep_date != None:
            ep_date = map(int,self._get_episode_date().split("-"))
            current_date = map(int,datetime.datetime.now().strftime("%Y-%m-%d").split("-"))
            if ep_date[0] > current_date[0]:
                return False
            elif ep_date[0] == current_date[0]:
                if ep_date[1] > current_date[1]:
                    return False
                elif ep_date[1] == current_date[1]:
                    if ep_date[2] > current_date[2]:
                        return False
                    return True
                return True
            else:
                return True
        else:
            return False

    def is_online(self):
        """
        if self._season < 10:
            if self._current_episode < 10:
                link="https://www.yggtorrent.is/engine/search?name="+self._name+"+S0"+str(self._season) + "E0" + str(self._current_episode)+"&description=720p&file=&uploader=&category=2145&sub_category=2184&do=search"  
                exp=re.compile("(.)*"+self.name.lower()+"(.)*s0"+str(self.current_s)+"e0"+str(self.current_ep)+"(.)*vostfr(.)*720p")
                br.open(lien)
                for link in br.links():
                    if re.search(exp,link.url):
                        print link.url
                        br.open(link.url)
                        return True
                return False
            elif self.current_ep>=10:
                lien="https://www.yggtorrent.is/engine/search?name="+self._name+"+S0"+ str(self._season) + "E" + str(self._current_episode)+"&description=720p&file=&uploader=&category=2145&sub_category=2184&do=search"
                br.open(lien)
                exp=re.compile("(.)*"+self.name.lower()+"(.)*s0"+str(self.current_s)+"e"+str(self.current_ep)+"(.)*vostfr(.)*720p")
                for link in br.links():
                    if re.search(exp,link.url):
                        print link.url
                        br.open(link.url)
                        return True
                return False
        else:
            if self.current_ep<10:
                lien="https://www.yggtorrent.is/engine/search?name="+self._name+"+S"+str(self._season) + "E0" + str(self._current_episode)+"&description=720p&file=&uploader=&category=2145&sub_category=2184&do=search"
                br.open(lien)
                exp=re.compile("(.)*"+self.name.lower()+"(.)*s"+str(self.current_s)+"e0"+str(self.current_ep)+"(.)*vostfr(.)*720p")
                for link in br.links():
                    if re.search(exp,link.url):
                        print link.url
                        br.open(link.url)
                        return True
                return False
            elif self.current_ep>=10:
                lien="https://www.yggtorrent.is/engine/search?name="+self._name+"+S"+str(self._season) + "E" + str(self._current_episode)+"&description=720p&file=&uploader=&category=2145&sub_category=2184&do=search"                
                br.open(lien)
                exp=re.compile("(.)*"+self.name.lower()+"(.)*s"+str(self.current_s)+"e"+str(self.current_ep)+"(.)*vostfr(.)*720p")
                for link in br.links():
                    if re.search(exp,link.url):
                        print link.url
                        br.open(link.url)
                        return True
                return False
        """
        return 0

    def download_torrent(self):
       for link in br.links():
            if re.search(r"download_torrent",link.url):
                content=br.open(link.url)
                with open(("Torrent"+self.name+"S"+str(self.current_s)+"E"+str(self.current_ep)),"wb") as torrent:
                    torrent.write(content.get_data())
        #self.update_episode()

    def update_current_data(self, ep=0):
        if (ep==0):
            self._set_current_ep_data(self._remaining_ep_data[0])
            self._set_remaining_ep_data(self._remaining_ep_data[1:])
        else:
            self._set_current_ep_data(self._remaining_ep_data[ep-self._current_episode-1])
            self._set_remaining_ep_data(self._remaining_ep_data[ep-self._current_episode:])
    
    def update_episode(self, ep=0):
        if self._current_episode == self._nb_episodes:
            if self._season == self._nb_seasons:
                self._end = True
            else:
                self._season += 1
                self._current_episode = 1
        else:
            if (ep == 0):
                self._current_episode += 1
                self.update_current_data()
            else:
                self.update_current_data(ep)
                self._current_episode = ep



