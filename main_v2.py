#-*- coding: utf-8 -*-
from Serie_v2 import *

import curses, os, time, pickle, signal, sys


global curseur,affi,series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info

#--- interface graphique ---

def init():

    global series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info

    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.cbreak()
    curses.noecho()
    screen.keypad(1)
    screen.nodelay(1)
    curses.curs_set(0) #curseur invisible

    dims = screen.getmaxyx()

    height_list = 2*dims[0]/3
    width_list = 4*dims[1]/7
    begin_x_list = dims[1]/30
    begin_y_list = dims[0]/8
    win_list = curses.newwin(height_list, width_list, begin_y_list, begin_x_list)

    height_info = dims[0]/3
    width_info = dims[1]/3
    begin_x_info = dims[1]-width_info - dims[1]/30
    begin_y_info = dims[0]/8
    win_info = curses.newwin(height_info,width_info,begin_y_info,begin_x_info)

def clear():
    global series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info
    screen.clear()
    win_list.clear()
    win_info.clear()

def draw_border():
    global series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info
    screen.border()
    win_list.border()
    win_info.border()

def draw_interface():
    global series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info
    screen.addstr(0,dims[1]/2-len(" Serie Downloader ")/2," Serie Downloader ",curses.A_REVERSE)
    screen.addstr(dims[0]- 2,1,"(A) Add")
    screen.addstr(dims[0]-2,dims[1]/2-len("(U) Update")/2,"(U) Update")
    screen.addstr(dims[0]- 2 ,dims[1]-len("(Q) Quit "),"(Q) Quit")
    win_list.addstr(0,width_list/2-len(" Prochaines Sorties ")/2," Prochaines Sorties ",curses.A_REVERSE)
    win_info.addstr(0,width_info/2-len(" Info ")/2," Info ",curses.A_REVERSE)

def refresh():
    global series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info
    screen.refresh()
    win_list.refresh()
    win_info.refresh()

def interact():
    global affi, curseur, series
    k = screen.getch()
    if k == ord("A") or k == ord("a"):
        pass
    elif k == ord("\n"):
        modif(series[curseur])
    elif k == curses.KEY_UP:
        curseur = (curseur - 1) % len(series)
    elif k == curses.KEY_DOWN:
        curseur = (curseur + 1) % len(series)
    elif k == ord("U") or k == ord("u"):
        force_update()
    elif k == ord("Q") or k == ord("q"):
        quit()

def affichage():
    global curseur, affi,series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info  
    i = 2
    affi = [0] * len(series)
    affi[curseur] = curses.A_REVERSE
    j=0
    for serie in series:
        win_list.addstr(i,1,serie._get_name() + " " + serie.show(),affi[j])
        win_list.addstr(i+1,1,"-"*(width_list-2))
        i+=2
        j+=1
    win_info.addstr(2,1,series[curseur]._get_name())

def modif(serie):
    k = 0
    ep=""
    while k != ord("\n"):
        i=2
        for s in series:
            win_list.refresh()
            win_info.refresh()
            win_list.nodelay(1)
            if s == serie:
                win_list.addstr(i,1,"Episode: " + ep,curses.A_REVERSE)
                k = win_list.getch()
                if k == curses.KEY_BACKSPACE:
                    ep = ep[:-1]
                elif k >= ord("0") and k <= ord("9"):
                    ep=ep+chr(k)
                else:
                    pass
            else:    
                win_list.addstr(i,1,s._get_name() + " " + s.show())
                win_list.addstr(i+1,1,"-"*(width_list-2))
            win_info.addstr(0,width_info/2-len(" Info ")/2," Info ",curses.A_REVERSE)
            win_info.addstr(2,1,series[curseur]._get_name())
            i+=2
    if(ep.isdigit() and ep>serie._get_current_episode):
        serie.update_episode(int(ep))

#--- Fonction principale ---

def run():
    global affi,series, dims, screen, height_list, width_list, height_info, width_info, begin_x_list, begin_y_list, begin_x_info, begin_y_info, win_list, win_info
    while 1:
        clear()
        draw_border()
        draw_interface()
        update()
        verification()
        interact()
        affichage()
        refresh()
        time.sleep(0.1)

def main():
    date_jour = datetime.datetime
    init()
    run()

def fermer_prog(signal,frame):
    quit()

def quit():
    curses.endwin()
    os.system("clear")
    print ("Sauvegarde en cours")
    with open("données","wb") as fichier:
        save = pickle.Pickler(fichier)
        save.dump(series)
    sys.exit(0)


def verification():
    for episode in series:
        if episode.is_out():
            if episode.is_online():
                download(episode)

def update():
    for serie in series:
        if datetime.datetime.now().month > serie._get_last_update().month:
            with open("MaJ","ab") as Maj:
                Maj.write("\n------ Update "+serie._get_name()+"------\n\n")
                serie.update_data()

def force_update():
    screen.nodelay(1)
    with open("MaJ","ab") as MaJ:
        MaJ.write("\n------ ForceUpdate ------\n\n")
    for serie in series:
        serie.update_data()

def download(episode):
    return 0
    #episode.download_torrent()


signal.signal(signal.SIGINT,fermer_prog)
curseur = 0

try:
    print ("Accès aux données en cours ...")
    with open("données","rb") as fichier:
        data = pickle.Unpickler(fichier)
        series = data.load()
except:
    print ("Erreur\nPas de données trouvées")
    Arrow=Serie("Arrow","tt2193021",7,1)
    Supergirl=Serie("Supergirl","tt4016454",2,14)
    LegendsOfTomorrow=Serie("Legends+of+Tomorrow","tt4532368",3,8)
    TheFlash=Serie("The+Flash+2014","tt3107288",5,1)
    Suits=Serie("Suits","tt1632701",7,3)
    Salvation = Serie("Salvation","tt6170874",2,9)
    GoodDoctor = Serie("Good+Doctor","tt6470478", 1,15)
    series=[Arrow,Supergirl,LegendsOfTomorrow,TheFlash,Suits,Salvation,GoodDoctor]


main()
