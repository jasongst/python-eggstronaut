#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from time import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import random,moveapi,time,urllib.request,json,urllib,tempfile,os
#from IA import graphIA

print("Lancement du jeu veuillez patienter ...")
class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()
        # test

    def initUI(self):
        # définition de la palette (exactement celle du cours)
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette()
        # couleur du bg de la window
        p.setColor(QPalette.Window, QColor(53,53,53))
        # couleur des boutons
        p.setColor(QPalette.Button, QColor(53,53,53))
        p.setColor(QPalette.Highlight, QColor(142,45,197))
        p.setColor(QPalette.ButtonText, QColor(255,255,255))
        p.setColor(QPalette.WindowText, QColor(255,255,255))
        self.mapalette=p
        self.setPalette(p)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gameVersion="1.0.6"
        self.initUI()

    def prepareicon(self):
        # définition de l'icon de la fenêtre
        imgicon = QIcon("./assets/img/icons/icon.png")
        return imgicon

    def initUI(self):
        # definition de la géométrie de ma fenetre
        self.gamerunning=False
        self.shift=False
        self.setGeometry(10, 10, 1280, 720)
        # on fixe la taille de la fenetre
        self.setFixedSize(1280,720)
        # on récupère l'icon
        self.icon=self.prepareicon()

        # on met le titre de la fenetre
        self.setWindowTitle('Eggstronaut Startup')
        # on envoie un message dans la barre de status
        self.statusBar().showMessage("Bienvenue !")
        # on définit l'icon
        self.setObjectName("masterwin")
        self.setWindowIcon(self.icon)
        # on permet l'envoie de notif push avec le qsystemtrayicon (utile)
        self.syicon=QSystemTrayIcon(self.icon,self)
        # on le rend visible
        self.syicon.setVisible(True)
        # on l'affiche
        self.syicon.show()
        self.mpStatus=False
        self.ctrl=False
        self.mpType=None
        self.setCenter()
        self.ping=0
        self.placebuttons()
        self.tempfolder=tempfile.gettempdir()
        #self.musicvolume=100
        self.effectvolume=100
        self.separateurst=":"
        self.player = QMediaPlayer()
        self.effectplayer=QMediaPlayer()
        if os.path.isfile(self.tempfolder+"/cfg_eggstronaut.cfg"):
            fic=open(self.tempfolder+"/cfg_eggstronaut.cfg","r")
            string = fic.read()
            if ":" not in string or len(string) == 0:
                print(string)
                fic.close()
                
                f=open(self.tempfolder+"/cfg_eggstronaut.cfg","w")
                f.write("100:100:0")
                f.close()
                self.musicvolume=100
                self.effectvolume=100
                self.settingsvalues = ["100","100","0"]
            else:   
                self.settingsvalues = string.split(":")
                self.musicvolume=int(self.settingsvalues[0])
                self.effectvolume=int(self.settingsvalues[1])
                
                fic.close()
        else:
            f=open(self.tempfolder+"/cfg_eggstronaut.cfg","w")
            f.write("100:100:0")
            self.musicvolume=100
            self.effectvolume=100
            self.settingsvalues = ["100","100","0"]
            f.close
        self.player.setVolume(self.musicvolume)
        self.effectplayer.setVolume(self.effectvolume)
        self.placeparambtn()

        # musique d'intro
        self.intromusique=QSound("./assets/sounds/music/menu.wav")
        self.intromusique.play()
        self.intromusique.setLoops(2147483647)

        self.setBG()
        self.show()
        if self.settingsvalues[2] == "1":
            self.fullscreen()

    def placebuttons(self):
        self.playbtnsolo=QPushButton("",self)
        # Application de la texture

        self.playbtnsolo.setFixedWidth(213)
        self.playbtnsolo.setObjectName("solobtn")
        self.playbtnsolo.setFixedHeight(56)
        self.setStyleSheet("#solobtn{ border-image: url(./assets/img/bg/solo1.png);} #solobtn:hover{ border-image: url(./assets/img/bg/solo2.png);} #multibtn{border-image: url(./assets/img/bg/multi1.png);}")



        self.playbtnsolo.setToolTip("Cliquez ici pour jouer au jeu !")
        self.playbtnsolo.move((self.width()/2-(self.playbtnsolo.width()/2)),416)
        self.playbtnsolo.show()
        self.playbtnsolo.clicked.connect(self.initGame)




        self.playbtnmulti=QPushButton("",self)
        self.playbtnmulti.setToolTip("Cliquez ici pour jouer au jeu en multi !")
        self.playbtnmulti.setObjectName("multibtn")
        self.playbtnmulti.setFixedWidth(213)
        self.playbtnmulti.setFixedHeight(56)

        self.playbtnmulti.move((self.width()/2-(self.playbtnmulti.width()/2)),491)
        self.playbtnmulti.show()
        self.playbtnmulti.setStyleSheet("#multibtn:hover{ border-image: url(./assets/img/bg/multi2.png);}")
        self.playbtnmulti.clicked.connect(self.MultiPlayer)


        self.creditbtn=QPushButton("",self)
        self.creditbtn.setFixedWidth(213)
        self.creditbtn.setFixedHeight(56)
        self.creditbtn.setToolTip("Cliquez ici pour les crédits")

        self.creditbtn.setObjectName("creditbtn")
        self.creditbtn.show()
        self.creditbtn.setStyleSheet("#creditbtn{ border-image: url(./assets/img/bg/credit1.png); } #creditbtn:hover{ border-image: url(./assets/img/bg/credit2.png);}")
        self.creditbtn.move((self.width()/2-(self.creditbtn.width()/2)),564)
        self.creditbtn.clicked.connect(self.creditWindow)





    def creditWindow(self):
        #print("credit")
        self.btnmusique=QSound("./assets/sounds/effects/btn1.wav")
        self.btnmusique.play()
        maCreditBox=QDialog(self)
        maCreditBox.setWindowTitle("Crédits")
        maCreditBox.setFixedWidth(900)
        maCreditBox.setFixedHeight(600)
        maCreditBox.setModal(True)
        # btn=QPushButton("&Fermer",maCreditBox)
        # btn.move((maCreditBox.width()/2-btn.width()/2),maCreditBox.height()-btn.height())
        # btn.clicked.connect(maCreditBox.close)
        maCreditBox.show()
        maCreditBox.setObjectName("credit")
        maCreditBox.setStyleSheet("#credit{background-image:url(./assets/img/bg/bg_credit.png) !important; background-color: rgb(53,53,53)}")


    def initGame(self):
        self.intromusique.stop()
        self.playbtnsolo.setEnabled(False)
        self.playbtnmulti.setEnabled(False)
        self.creditbtn.setEnabled(False)
        self.btnmusique=QSound("./assets/sounds/effects/btn1.wav")
        self.btnmusique.play()
        self.playerId="1"
        self.carte=createGameMap()
        #self.ajoutBTN()

        self.startup()
        self.carte=prepareGame(self.nbPlayers,self.carte,False)


    def MultiPlayer(self):
        self.btnmusique=QSound("./assets/sounds/effects/btn1.wav")
        self.btnmusique.play()
        self.intromusique.stop()
        if self.shift:
            self.shift=False
            self.debugmode()
        elif self.ctrl:
            self.testMPavail(othersrv=True)
        else:
            self.testMPavail()
    def testMPavail(self,othersrv=False):
        if othersrv:
            connectok=False
            while not connectok:
                self.ipthought, ok = QInputDialog.getText(self, 'Multiplayer', "Veuillez entrer l'adresse ip du serveur (avec http).\nSur ce serveur, le fichier requests.php doit se trouver dans le dossier /1iut/tutoreS2 !")
                if ok:
                    try:
                        response = urllib.request.urlopen(self.ipthought+'/1iut/tutoreS2/requests.php?act=getver').read().decode("utf8")
                        self.srvdomain=self.ipthought
                        avail=True
                        connectok=True
                    except:
                        errbox=QMessageBox.critical(self,"Erreur!","L'adresse que vous avez entré semble être fausse, ou bien le serveur est arrêté!\n Veuillez recommencer!",QMessageBox.Ok)
                        connectok=False
        else:
            print("Test connexion serveur virgile")
            self.statusBar().showMessage("Veuillez patienter ... connexion au serveur (essai hors local)")
            try:
                response = urllib.request.urlopen('http://390-server/1iut/tutoreS2/requests.php?act=getver').read().decode("utf8")
                self.srvdomain="http://390-server"
                avail=True
            except:
                self.statusBar().showMessage("Veuillez patienter ... connexion au serveur (essai en local)")
                print("Connexion Locale impossible! Essai hors local...")
                avail=False
            if avail == False:
                try:
                    response = urllib.request.urlopen('https://virgile62150.ddns.net/1iut/tutoreS2/requests.php?act=getver').read().decode("utf8")
                    self.srvdomain="https://virgile62150.ddns.net"
                except:
                    self.srvdomain, ok = QInputDialog.getText(self, 'Multiplayer', "Aucune connexion n'est possible avec les serveurs de test, veuillez entrer votre nom de domaine")
                    try:
                        response = urllib.request.urlopen(self.srvdomain+'/1iut/tutoreS2/requests.php?act=getver').read().decode("utf8")
                    except:
                        errbox=QMessageBox.critical(self,"Erreur!","Impossible de se connecter au serveur. Essayez en solo!",QMessageBox.Ok)
                        self.initGame()
            jsoninfoserv=json.loads(response)
            if jsoninfoserv["server_version"] != self.gameVersion:
                info=QMessageBox.critical(self,"Erreur!","La version du serveur ne correspond pas à la version que vous utilisez!\nClient : "+self.gameVersion+" | Serveur : "+jsoninfoserv['server_version'])
                sys.exit(0)
        self.initGameMP()


    def initGameMP(self):
        self.nbPlayers=4
        self.playbtnsolo.setEnabled(False)
        self.playbtnmulti.setEnabled(False)
        self.userpseudo, ok = QInputDialog.getText(self, 'Multiplayer', 'Afin de jouer en multijoueur, vous devez entrer un pseudo')
        if ok:

            self.choosedial=QDialog()
            existing=QPushButton("Connecter",self.choosedial)
            existing.clicked.connect(self.connectsrv)
            create=QPushButton("Créer une partie",self.choosedial)
            create.clicked.connect(self.preparesrv)
            existing.move(0,0)
            self.choosedial.setWindowTitle("Connexion")
            self.choosedial.setWindowFlags(Qt.WindowTitleHint)
            create.move(100,0)
            self.choosedial.setWindowModality(Qt.ApplicationModal)
            self.choosedial.exec_()

            #self.ajoutBTN()
            #self.preparesrv()
            #self.startup()
            #self.initGameMP()
            if self.mpStatus:
                self.carte=prepareGame(self.nbPlayers,self.carte,True)
            else:
                self.initGameMP()
        else:
            self.initGameMP()

    def connectsrv(self):
        self.choosedial.close()
        # Demande à l'utilisateur de rentrer l'id de sa partie
        idfaux=True
        while idfaux:
            try:
                partie, ok = QInputDialog.getText(self, 'Multiplayer', "Veuillez entrer l'identifiant de la partie")
                self.idP=int(partie)
            except:
                errbox=QMessageBox.critical(self,"Erreur!","Qu'on soit d'accord entre nous, L'IDENTIFIANT DE LA PARTIE EST UNIQUEMENT COMPOSÉ DE NOMBRES, PAS DE TEXTE OU AUTRE!!!!!",QMessageBox.Ok)
                self.connectsrv()
            # vérification de l'id de la partie ...
            try:
                request=urllib.request.urlopen(self.srvdomain+"/1iut/tutoreS2/requests.php?act=getmap&idP="+str(self.idP)).read().decode("utf8")
                playerid=urllib.request.urlopen(self.srvdomain+"/1iut/tutoreS2/requests.php?act=addplayer&idP="+str(self.idP)).read().decode("utf8")
                plid=json.loads(playerid)
                self.playerId=str(plid['player_id'])
                #newmap=json.loads(request)
                # print(newmap)
                # if "error" in newmap:
                #     Erreur=QMessageBox.critical(self,"Erreur!","Le serveur à retourné l'erreur suivante :"+json_req['error'],QMessageBox.Ok)
                #     sys.exit(0)
            except:
                Erreur=QMessageBox.critical(self,"Erreur!","La synchro avec le serveur a été perdue! (1)",QMessageBox.Ok)
                sys.exit(0)
            data=json.loads(request)
            if "error" not in data:
                idfaux=False
                self.mpStatus=True
                self.mpType="client"
                self.carte=data[0]
                self.bb=data[1]
                self.nbPlayers=4

                self.bombeposee=[False,0]
                #self.bb=[]
                self.essai=0
                self.starta()

            else:
                msg=QMessageBox.critical(self,"Erreur!",data['error'],QMessageBox.Ok)


    def preparesrv(self):
        self.choosedial.close()
        self.nbPlayers=4
        self.bombeposee=[False,0]
        self.bb=[]
        self.playerId="1"
        self.essai=0
        self.carte=createGameMap()
        self.carte=prepareGame(self.nbPlayers,self.carte,True)
        # Création de la partie auprès du serveur avec la map choisie...
        mesdonnees=[self.carte,self.bb]
        cartesrv=json.dumps(mesdonnees)
        datas={"data":cartesrv}
        data=urllib.parse.urlencode(datas).encode()
        request=urllib.request.urlopen(self.srvdomain+"/1iut/tutoreS2/requests.php?act=creategame",data=data).read().decode("utf8")
        json_req=json.loads(request)
        self.idP=json_req['id_partie']
        if "error" not in json_req:
            info=QMessageBox.information(self,"Multiplayer","La partie à bien été créée, notez votre identifiant de partie : "+str(json_req['id_partie'])+" (celui ci sera affiché dans la barre de status)")
            self.mpStatus=True
            self.mpType="host"
        else:
            Erreur=QMessageBox.critical(self,"Erreur!","Le serveur à retourné l'erreur suivante :"+json_req['error'],QMessageBox.Ok)
            self.initGame()
        self.syicon.showMessage("EggStronaut - MultiJoueur","Félicitations! Votre partie en ligne est créée "+self.userpseudo+"! Les autres joueurs peuvent rejoindre la partie avec le code suivant : "+str(json_req['id_partie'])+".",icon=QSystemTrayIcon.Information,msecs=1000)
        self.starta()

    def setBG(self):
        #self.setStyleSheet("#masterwin{background-image: url('./assets/img/bg/screen.png'); background-size: cover }")
        self.setStyleSheet("#masterwin{border-image: url('./assets/img/bg/screen.png') 0 0 0 0 stretch stretch; }")        
    def setnewBG(self):
        #self.setStyleSheet("#masterwin{background-image: url('./assets/img/bg/ingame_bg.png'); background-size: cover }")
        self.setStyleSheet("#masterwin{border-image: url('./assets/img/bg/ingame_bg.png') 0 0 0 0 stretch stretch; }")

    def ajoutBTN(self):
        self.oneplayerbtn=QPushButton(self)
        self.oneplayerbtn.setText("1 Joueur")
        self.oneplayerbtn.move((self.width()-self.oneplayerbtn.width())/2,(self.height()-self.oneplayerbtn.height())/2)
        self.oneplayerbtn.show()
        self.oneplayerbtn.clicked.connect(self.oneplayer)


    def debugmode(self):
        played=False
        debugdialog=QDialog(self)
        debugdialog.setModal(True)
        debugdialog.setWindowTitle("Debug Mode")
        debugdialog.setFixedSize(720,480)

        label1=QLabel("Bienvenue dans le menu de déboguage",debugdialog)
        label1.move(0,0)
        label1.show()

        def testMusique():
            global played
            try:
                played
            except:
                played=False
            if not played:
                self.player.setMedia(QMediaContent(QUrl("./assets/sounds/music/08.mp3")))
                self.player.play()
                messagebox=QMessageBox.information(debugdialog,"Information","Test de la musique MP3 avec QMediaPlayer")
                
                played=True
            else:
                played=False
                self.player.stop()
        def testConnectionServeur():
            try:
                response = urllib.request.urlopen('http://390-server/1iut/tutoreS2/requests.php?act=getver').read().decode("utf8")
                data=json.loads(response)
                message="Connexion réussie sur le réseau local ! Version du serveur :"+data['server_version']
            except:
                try:
                    response = urllib.request.urlopen('http://390-server/1iut/tutoreS2/requests.php?act=getver').read().decode("utf8")
                    data=json.loads(response)
                    message="Connexion réussie via le serveur ddns ! Version du serveur :"+data['server_version']
                except:
                    message="Aucune connexion avec le serveur n'est possible (vérifiez votre connexion internet) ou peut être que le serveur est down."
            info=QMessageBox.information(debugdialog,"Test Connexion",message,QMessageBox.Ok)

        btn1=QPushButton(debugdialog)
        btn1.setText("Joueur musique")
        btn1.move(0,label1.height()+2)
        btn1.clicked.connect(testMusique)
        btn1.show()

        btn2=QPushButton(debugdialog)
        btn2.setText("Test Connexion")
        btn2.move(btn1.width()+2, label1.height()+2)
        btn2.clicked.connect(testConnectionServeur)
        btn2.show()

        label2=QLabel("Bien évidemment, comme vous êtes arrivé ici,\nvous vous doutez bien qu'il va y avoir une easter egg\nsinon ça ne serait pas drôle mais bon, je m'emporte 😂😂\nvoici le site sur lequel j'ai récupéré 90% des chansons:\nhttps://www.vob-clip.com/ attention, c'est en russe !!",debugdialog)
        label2.move(0,label1.height()+btn1.height()+2)
        label2.show()
        debugdialog.setFixedSize(label2.width()+5,label1.height()+btn1.height()+label2.height()+5)

        debugdialog.show()



    def startup(self):
        self.nbPlayers=2
        self.bombeposee=[False,0]
        self.bb=[]
        self.essai=0
        # while self.nbPlayers > 4 or self.nbPlayers <= 0:
        #     self.nbPlayers,self.ok=QInputDialog.getInt(self, "Entrez le nombre de joueurs","Entrez un nombre entre 1 et 4")
        self.carte=prepareGame(self.nbPlayers,self.carte,False)
        self.starta()


    def starta(self):
        self.bb=[]
        print(str(self.nbPlayers)+" souhaitent jouer ...")
        print("Initialisation de la fenêtre principale ...")
        self.statusBar().showMessage(str(self.nbPlayers)+" Joueur(s)")
        self.labelNbJoueurs=QLabel(self)
        self.labelNbJoueurs.setText("Eggstronaut Alpha "+self.gameVersion+" \n"+str(self.nbPlayers)+" Joueur(s)")
        self.labelNbJoueurs.move(969,660)
        self.labelNbJoueurs.setFixedWidth(254)
        self.labelNbJoueurs.show()
        self.statusBar().showMessage("Génération de la carte ...")
        self.statusBar().showMessage("Carte prête")
        self.setZoneJeu()



        self.dlFinished=True

        self.nonfabien=[QPixmap("./assets/img/menu/itm_fabien_unav.png"),"Vous n'avez pas encore récupéré l'item 'Fabien'."]
        self.ouifabien=[QPixmap("./assets/img/menu/itm_fabien_av.png"),"Vous pouvez executer l'attaque de Fabien en appuyant sur la touche F!"]

        self.nonrmv = [QPixmap("./assets/img/menu/itm_rmv_unav.png"),"Vous n'avez pas encore récupéré l'item Spam Bombes"]
        self.ouirmv = [QPixmap("./assets/img/menu/itm_rmv_av.png"),"Vous avez récupéré l'item Spam Bombes, il est actif !"]

        self.ouink = [QPixmap("./assets/img/menu/itm_nuke_av.png"),"VOUS AVEZ LA NUKE! avec cet item, la victoire est instantanée !!! Appuyer sur la touche N!"]
        # pas de cas contraire, l'item doit rester plus ou moins secret !

        self.setnewBG()
        self.sbar=0
        self.mabombe=False
        self.mesitems=[]
        self.olditemlist=[]
        self.bombCdDisabled=False

        # itembar
        self.itembarfab=QLabel(self)
        self.itembarfab.move(65,659)
        self.itembarfab.setPixmap(self.nonfabien[0])
        self.itembarfab.setToolTip(self.nonfabien[1])
        self.itembarfab.setFixedSize(QSize(49,30))


        self.itembarrmv=QLabel(self)
        self.itembarrmv.move(126,659)
        self.itembarrmv.setFixedSize(49,30)
        self.itembarrmv.setPixmap(self.nonrmv[0])
        self.itembarrmv.setToolTip(self.nonrmv[1])

        self.itembarnk=QLabel(self)
        self.itembarnk.move(185,659)
        self.itembarnk.setFixedSize(49,30)


        self.posbbexp=[]

        







        # le player est initialisé avant ^^
        if sys.platform != "linux" and sys.platform !="darwin":
            self.isLinux=False
            self.myMusicPlaylist=QMediaPlaylist()
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/01.mp3")))
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/02.mp3")))
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/03.mp3")))
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/04.mp3")))
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/05.mp3")))
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/06.mp3")))
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/07.mp3")))
            self.myMusicPlaylist.addMedia(QMediaContent(QUrl("./assets/sounds/music/08.mp3")))
            self.myMusicPlaylist.setPlaybackMode(QMediaPlaylist.Loop)
            self.myMusicPlaylist.setPlaybackMode(QMediaPlaylist.Random)
            self.player.setPlaylist(self.myMusicPlaylist)
            self.player.play()


        else:
            self.isLinux=True






        self.qurlNuke=QUrl("./assets/sounds/effects/nuke.mp3")


        # ----------------------------------------------
        # PARTIE IMPORTANTE DU CODE 
        # ENSEMBLE DES BOUCLES DE LA PARTIE
        # ----------------------------------------------



        # Boucle récupérant les appuis du joueur
        self.checkThreadTimer =QTimer(self)
        self.checkThreadTimer.setInterval(16) #.016 seconds
        self.checkThreadTimer.timeout.connect(self.bougeplayer)
        self.checkThreadTimer.start()

        # Boucle gérant les fabiens, quand l'item est activé
        self.checkThreadTimerFAB =QTimer(self)
        self.checkThreadTimerFAB.setInterval(1000) #1 second
        self.checkThreadTimerFAB.timeout.connect(self.chkfabien)

        # Boucle du bot si le joueur n'est pas en multijoueur
        if(self.nbPlayers>1) and not self.mpStatus:
            self.checkThreadTimerbot =QTimer(self)
            self.checkThreadTimerbot.setInterval(500) #.5 seconds
            self.checkThreadTimerbot.timeout.connect(self.bougebot)
            self.checkThreadTimerbot.start()

        # Boucle pour le changement d'information de la barre de status
        self.checkThreadTimerSB =QTimer(self)
        self.checkThreadTimerSB.setInterval(2000)
        self.checkThreadTimerSB.timeout.connect(self.changestatusbarmsg)
        self.checkThreadTimerSB.start()

        # Boucle s'occupant de la mise à jour de la carte en multijoueur
        if (self.mpStatus):
            self.checkThreadTimerMP =QTimer(self)
            self.checkThreadTimerMP.setInterval(100)
            self.checkThreadTimerMP.timeout.connect(self.getUpdMap)
            self.checkThreadTimerMP.start()


        # Boucle de vérification de victoire ou défaite du joueur
        self.checkThreadTimerVictory=QTimer(self)
        self.checkThreadTimerVictory.setInterval(500)
        self.checkThreadTimerVictory.timeout.connect(self.verifvictoire)
        self.checkThreadTimerVictory.start()


        # Boucle de vérification des items du joueur (pour les mettres dans la barre prévue à cet effet)
        self.checkThreadTimerItems=QTimer(self)
        self.checkThreadTimerItems.setInterval(2)
        self.checkThreadTimerItems.timeout.connect(self.updateitems)
        self.checkThreadTimerItems.start()


        # Timer (et pas boucle) lancant l'explosion de la bombe
        self.activebombe=QTimer(self)
        self.activebombe.setInterval(500)
        self.activebombe.timeout.connect(self.disablebomb)


        # Timer (et pas boucle) de la désactivation de 1 bombe à la fois (item 'rmv')
        self.bombCd = QTimer(self)
        self.bombCd.setInterval(4000)
        self.bombCd.timeout.connect(self.disableCd)


        # Boucle nettoyant la carte en cas de bug avec une bombe
        self.cleanupexp=QTimer(self)
        self.cleanupexp.setInterval(1000)
        self.cleanupexp.timeout.connect(self.cleanupmap)
        self.cleanupexp.start()

        # Timer de la nuke (laisse 3 secondes de patience avant l'explosion)
        self.nuke=QTimer(self)
        self.nuke.setInterval(3000)
        self.nuke.timeout.connect(self.nukemap)

        
        self.placeparambtn()

        self.fab_act=0
        self.fabienActif=True
        self.itembarfab.show()
        self.itembarrmv.show()
        self.itembarnk.show()

        self.gamerunning=True
        if self.isFullScreen():
            self.replaceelements(True)


    def getUpdMap(self):
        #self.carte=self.getMapStatus()
        
        if self.dlFinished:
            self.dlFinished=False
            try:
                request=urllib.request.urlopen(self.srvdomain+"/1iut/tutoreS2/requests.php?act=getmap&idP="+str(self.idP)).read().decode("utf8")
                newmap=json.loads(request)
                if "error" not in newmap:
                    self.carte=newmap[0]
                    self.bb=newmap[1]

                else:
                    Erreur=QMessageBox.critical(self,"Erreur!","Le serveur à retourné l'erreur suivante :"+json_req['error'],QMessageBox.Ok)
                    sys.exit(0)
            except:
                Erreur=QMessageBox.critical(self,"Erreur!","La synchro avec le serveur a été perdue! (2)",QMessageBox.Ok)
                self.gamerunning=False
                sys.exit(0)
            self.dlFinished=True
            self.drawNewMap(dl=True)
            
    def senfUpdMap(self,carte):
        #self.getMap()
        mesdonnees=[carte,self.bb]
        cartesrv=json.dumps(mesdonnees)
        datas={"data":cartesrv}
        data=urllib.parse.urlencode(datas).encode()
        temp=time.time()
        try:
            request=urllib.request.urlopen(self.srvdomain+"/1iut/tutoreS2/requests.php?act=updmap&idP="+str(self.idP),data=data).read().decode("utf8")
            temp2=time.time()
            self.ping=temp2-temp
            #newmap=json.loads(request)
            # print(newmap)
            # if "error" in newmap:
            #     Erreur=QMessageBox.critical(self,"Erreur!","Le serveur à retourné l'erreur suivante :"+json_req['error'],QMessageBox.Ok)
            #     sys.exit(0)
        except:
            Erreur=QMessageBox.critical(self,"Erreur!","La synchro avec le serveur a été perdue! (3)",QMessageBox.Ok)
            self.gamerunning=False
            sys.exit(0)
    def changestatusbarmsg(self):
        if self.sbar==0:
            if not self.isLinux:
                defmsg="Musique Actuelle : "
                indexM=self.myMusicPlaylist.currentIndex()
                if indexM == 0:
                    message = defmsg+"Flash & The Pan - Midnight Man (Extended)"
                elif indexM == 1:
                    message = defmsg+"Level 42 - Hot Water (Master Mix)"
                elif indexM == 2:
                    message = defmsg+"Billy Idol - Hot In The City"
                elif indexM == 3:
                    message = defmsg+"Bag Raiders - Shooting Stars"
                elif indexM == 4:
                    message = defmsg+"Frankie Goes To Hollywood - Two Tribes (Annihilation Mix)"
                elif indexM == 5:
                    message = defmsg+"Sweet - Love is like Oxygen"
                elif indexM == 6:
                    message = defmsg+"Whitesnake - Is This Love"
                elif indexM == 7:
                    message = defmsg+"Jermaine Stewart - Get Lucky"
                else:
                    message = "Aucune background musique en lecture !"
            else:
                message = "Les Musiques ne fonctionnent pas sur Linux !"
            self.sbar=1
            self.statusBar().showMessage(message)
        elif self.sbar==1 and not self.mpStatus:
            self.statusBar().showMessage("Partie en cours !")
            self.sbar=0
        elif self.sbar==1 and self.mpStatus:
            self.statusBar().showMessage("Partie MultiPlayer en cours ... (Code :"+str(self.idP)+" )")
            self.sbar=2
        elif self.sbar==2 and self.mpStatus:
            ping=self.ping*1000
            self.statusBar().showMessage("Ping avec le serveur : "+str(int(ping))+" ms.")
            self.sbar=0






    def placeparambtn(self):
        #imagesettings=QPixmap("./assets/img/icons/settings.png")
        #icon=QIcon(imagesettings)


        self.settingsbtn=QPushButton(self)
        self.settingsbtn.move(8,10)
        self.settingsbtn.setFixedSize(QSize(46,46))
        self.settingsbtn.setObjectName("settings")
        self.settingsbtn.setStyleSheet("#settings {border-image: url(./assets/img/bg/tool1.png);}#settings:hover {border-image: url(./assets/img/bg/tool2.png);}")
        #self.settingsbtn.setIcon(icon)
        self.settingsbtn.show()
        self.settingsbtn.clicked.connect(self.settings)
    def settings(self):
        self.settingsDialog=QDialog(self)
        self.settingsDialog.setModal(True)
        self.settingsDialog.setObjectName("settingsWin")
        self.settingsDialog.setStyleSheet("#settingsWin {background-image:url(./assets/img/bg/bg_param.png); }")
        self.settingsDialog.setFixedSize(426,240)
        volumeaudiolbl=QLabel(self.settingsDialog)
        volumeeffetlbl=QLabel(self.settingsDialog)
        self.settingsDialog.setWindowTitle("Paramètres")
        volumeaudiolbl.setText("Volume Musique : ")
        volumeeffetlbl.setText("Volume Effets  : ")
        volumeaudiolbl.move(0,0)
        volumeeffetlbl.move(0,volumeaudiolbl.height())
        self.niveauvolumelbl = QLabel(self.settingsDialog)
        self.niveaueffetlbl = QLabel(self.settingsDialog)
        self.niveauvolumelbl.setFixedWidth(40)
        self.niveaueffetlbl.setFixedWidth(40)
        self.volumeslider=QSlider(Qt.Horizontal,self.settingsDialog)
        self.effetslider=QSlider(Qt.Horizontal,self.settingsDialog)
        self.niveauvolumelbl.move(volumeaudiolbl.width()+self.volumeslider.width(),0)
        self.niveaueffetlbl.move(volumeeffetlbl.width()+self.effetslider.width(),volumeaudiolbl.height())
        self.volumeslider.setTickInterval(101)
        self.effetslider.setTickInterval(101)
        self.volumeslider.setSingleStep(1)
        self.effetslider.setSingleStep(1)
        self.volumeslider.move(volumeaudiolbl.width()+5,0)
        self.effetslider.move(volumeeffetlbl.width()+5,volumeaudiolbl.height())
        self.volumeslider.valueChanged[int].connect(self.chgvol)
        self.effetslider.valueChanged[int].connect(self.chgeff)
        self.volumeslider.setValue(self.musicvolume)
        self.effetslider.setValue(self.effectvolume)


        # Si la taille de l'écran est inférieure ou égale à 1366x768
        masize=QSize(qApp.screens()[0].size())
        if True:#masize.height() <= 768 or masize.width() <= 1366:
            self.fullscreenbtn=QPushButton(self.settingsDialog)
            self.fullscreenbtn.setText("Plein Écran")
            self.fullscreenbtn.move(233,self.niveaueffetlbl.height()+volumeaudiolbl.height()+2)
            self.fullscreenbtn.clicked.connect(self.fullscreen)
            self.fullscreenbtn.show()


        self.effetslider.show()
        self.volumeslider.show()

        # ajout des boutons mp
        if self.mpStatus:
            closepartie=QPushButton(self.settingsDialog)
            closepartie.setText("Quitter le serveur")
            closepartie.move(0,self.niveaueffetlbl.height()+volumeaudiolbl.height()+2)
            closepartie.clicked.connect(self.disconnect)
            closepartie.show()
        else:
            closepartie=QPushButton(self.settingsDialog)
            closepartie.setText("Quitter le jeu")
            closepartie.move(0,self.niveaueffetlbl.height()+volumeaudiolbl.height()+2)
            closepartie.clicked.connect(self.quit)
            closepartie.show()







        self.settingsDialog.show()


    def fullscreen(self):
        # try:
        #     self.settingsDialog
        #     message=QMessageBox.information(self.settingsDialog,"Information", "Vous disposez d'un écran d'une résolution inférieure ou égale à 1366x768, en passant en plein écran, certains élèments risquent de ne pas être affichés correctement !",QMessageBox.Ok)
        # except:
        #     None
        if not self.isFullScreen():
            self.settingsvalues[2]="1"
            self.showFullScreen()
        else:
            self.settingsvalues[2]="0"
            self.showNormal()
        f=open(self.tempfolder+"/cfg_eggstronaut.cfg","w")
        f.write(self.separateurst.join(self.settingsvalues))
        f.close
        self.replaceelements(self.gamerunning)


    def replaceelements(self,game):
        if game:
            #self.settingsbtn.move(0,0)
            self.itembarnk.move(self.width()*0.14453125,self.height()*0.915277778)
            self.itembarnk.setFixedSize(self.width()*0.03828125,self.height()*0.041666667)
            self.itembarrmv.move(self.width()*0.0984375,self.height()*0.915277778)
            self.itembarrmv.setFixedSize(self.width()*0.03828125,self.height()*0.041666667)
            self.itembarfab.move(self.width()*0.05078125,self.height()*0.915277778)
            self.itembarfab.setFixedSize(self.width()*0.03828125,self.height()*0.041666667)
            self.labelNbJoueurs.move(self.width()*0.75703125,self.height()*0.916666667)
            self.labelNbJoueurs.setFixedWidth(self.width()*0.1984375)

            # debug ...
            self.creditbtn.hide()
            self.playbtnsolo.hide()
            self.playbtnmulti.hide()


        else:
            self.creditbtn.move((self.width()/2-(self.creditbtn.width()/2)),self.height()*0.783333333)
            self.playbtnsolo.move((self.width()-self.playbtnsolo.width())/2,self.height()*0.577777778)
            self.playbtnmulti.move((self.width()/2-(self.playbtnmulti.width()/2)),self.height()*0.681944444)

    def disconnect(self):
        self.checkThreadTimerMP.stop()
        if self.mpType=="host":
            try:
                request=urllib.request.urlopen(self.srvdomain+"/1iut/tutoreS2/requests.php?act=deletegame&idP="+str(self.idP)).read().decode("utf8")
                ifo=json.loads(request)
                if "OK" in ifo:
                    info=QMessageBox.information(self,"Multiplayer",ifo['OK'])
                    self.quit()
                else:
                    Erreur=QMessageBox.critical(self,"Erreur!","Le serveur à retourné l'erreur suivante :"+ifo['error'],QMessageBox.Ok)
            except:
                #Erreur=QMessageBox.critical(self,"Erreur!","La synchro avec le serveur a été perdue! (4)",QMessageBox.Ok)
                self.quit()
        else:
            sys.exit(0)

    def quit(self):
        sys.exit(0)


    def chgvol(self,value):
        self.niveauvolumelbl.setText(str(value+1)+" %")
        self.musicvolume=value
        self.settingsvalues[0]=str(self.musicvolume)
        f=open(self.tempfolder+"/cfg_eggstronaut.cfg","w")
        f.write(self.separateurst.join(self.settingsvalues))
        f.close
        self.player.setVolume(value)

    def chgeff(self,value):
        self.niveaueffetlbl.setText(str(value+1)+" %")
        self.effectvolume=value
        self.settingsvalues[1]=str(self.effectvolume)
        f=open(self.tempfolder+"/cfg_eggstronaut.cfg","w")
        f.write(self.separateurst.join(self.settingsvalues))
        f.close
        self.effectplayer.setVolume(value)




    def keyPressEvent(self,event):
        self.shift=False
        key = event.key()
        if self.gamerunning:
            if (key == Qt.Key_Q):
                self.getMap()
                self.carte, self.mesitems=moveapi.moveleft(self.carte,self.playerId,self.mesitems)
                self.drawNewMap()
            elif (key == Qt.Key_D):
                self.getMap()
                self.carte, self.mesitems=moveapi.moveright(self.carte,self.playerId,self.mesitems)
                self.drawNewMap()
            elif key == Qt.Key_Z:
                self.getMap()
                self.carte, self.mesitems=moveapi.moveup(self.carte,self.playerId,self.mesitems)
                self.drawNewMap()
            elif key == Qt.Key_S:
                self.getMap()
                self.carte, self.mesitems=moveapi.movedown(self.carte,self.playerId,self.mesitems)
                self.drawNewMap()
            elif key == Qt.Key_N:
                self.getMap()
                if "nk" in self.mesitems:
                    self.mesitems.remove("nk")
                    self.itembarnk.hide()
                    
                    
                    # on reprend des effets de posebombe
                    zz=moveapi.posebombe(self.playerId,self.carte)
                    self.bb.append([zz[1],time.time(),True])
                    self.bombeposee=[True,time.time()]


                    self.effectplayer.setMedia(QMediaContent(self.qurlNuke))
                    self.effectplayer.play()
                    self.nuke.start()
                    self.drawNewMap()
                else:
                    self.statusBar().showMessage("Vous n'avez pas l'item Nuke !")
            # elif key == Qt.Key_R:
            #     self.carte=createGameMap()
            #     self.carte=prepareGame(self.nbPlayers,self.carte,self.mpStatus)
            #     self.drawNewMap()
            elif key == Qt.Key_F:
                self.getMap()
                if "ifb" in self.mesitems:
                    self.mesitems.remove("ifb")
                    act=moveapi.elevage_de_moi(self.carte,self.playerId,self.fab_act)
                    self.carte=act[0]
                    self.fab_act=act[1]
                    self.fabien=act[2]
                    self.drawNewMap()
                    self.checkThreadTimerFAB.start()

                else:
                    self.statusBar().showMessage("Vous n'avez pas l'item Fabien !")

            elif key == Qt.Key_B:
                if not self.mabombe or self.bombCdDisabled:
                    self.mabombe=True
                    zz=moveapi.posebombe(self.playerId,self.carte)
                    self.bb.append([zz[1],time.time(),False])
                    self.drawNewMap()
                    self.bombeposee=[True,time.time()]
                else:
                    self.statusBar().showMessage("Attendez que l'autre bombe explose !!!!")
            elif key == Qt.Key_F2:
                self.myMusicPlaylist.next()
                self.player.play()

        if key == Qt.Key_Escape:
            self.settings()
        elif key == Qt.Key_Shift:
            self.shift=True
        elif key == Qt.Key_Control:
            self.ctrl=True

    def updateitems(self):
        if len(self.mesitems) != len(self.olditemlist):
            if len(self.mesitems)>len(self.olditemlist):
                self.statusBar().showMessage("Vous venez de récuperer l'item "+self.mesitems[len(self.mesitems)-1])
            for i in self.mesitems:
                if i == "ifb":
                    self.itembarfab.setPixmap(self.ouifabien[0])
                    self.itembarfab.setToolTip(self.ouifabien[1])
                elif i == "ex":
                    pos=moveapi.getPos(self.playerId,self.carte)
                    self.carte[pos[0]][pos[1]]=" "
                elif i == "rmv":
                    self.bombCdDisabled=True
                    self.itembarrmv.setPixmap(self.ouirmv[0])
                    self.itembarrmv.setToolTip(self.ouirmv[1])
                    self.mesitems.remove("rmv")
                    self.bombCd.start()
                elif i == "nk":
                    self.itembarnk.setPixmap(self.ouink[0])
                    self.itembarnk.setToolTip(self.ouink[1])
            if "ifb" not in self.mesitems:
                self.itembarfab.setPixmap(self.nonfabien[0])
                self.itembarfab.setToolTip(self.nonfabien[1])
            self.updateold()
        
        
        if len(self.bb) == 0 and self.mabombe:
            self.mabombe=False
        
        # débogage en cas de glitch (workaround)

    def nukemap(self):
        self.carte=moveapi.nuke(self.carte,self.playerId)
        self.nuke.stop()
        self.drawNewMap()
        


    def cleanupmap(self):
        # permet de nettoyer la map si une bombe explosée ne s'est pas dégagée

        self.getMap()
        rep=moveapi.removeoldexplosions(self.carte,self.bb)
        if rep[0]:
            self.carte=rep[1]
            self.drawNewMap()



    def updateold(self):
        self.olditemlist=[]
        for i in self.mesitems:
            self.olditemlist.append(i)

    def verifvictoire(self):
        self.getMap()
        otherusers=["1","2","3","4"]
        actualuser=self.playerId
        otherusers.remove(actualuser)
        otherusersalive=False
        actualuseralive=False
        for i in self.carte:
            for j in i:
                if j == actualuser:
                    actualuseralive=True
                if j in otherusers:
                    otherusersalive=True
        if not actualuseralive:
            self.checkThreadTimer.stop()
            self.checkThreadTimerVictory.stop()
            
            
            #quitbtn.hide()
            if self.mpStatus:
                errbox=QMessageBox.critical(self,"Game Over!","Fin de la partie. Vous êtes mort. Mais vous pouvez continuer de visualiser la partie",QMessageBox.Ok)
                self.gamerunning=False
            else:
                #errbox=QMessageBox.critical(self,"Game Over!","Fin de la partie. Vous êtes mort.",QMessageBox.Ok)

                self.checkThreadTimerbot.stop()
                self.checkThreadTimerVictory.stop()
                defeat=QPixmap("./assets/img/menu/defeat.png")
                udead=QLabel(self)
                udead.move(self.width()/2-1156/2,self.height()/2-594/2-12)
                udead.setFixedSize(1156,594)
                udead.setPixmap(defeat)
                udead.show()
                quitbtn=QPushButton(self)
                quitbtn.setObjectName("quitbtn")
                quitbtn.setFixedSize(213,56)
                quitbtn.setStyleSheet("#quitbtn { border-image: url(./assets/img/bg/quit_d.png);} #quitbtn:hover { border-image: url(./assets/img/bg/quithovered.png);}")
                quitbtn.move(self.width()*0.415234375,self.height()*0.811111111)
                quitbtn.clicked.connect(self.quit)
                quitbtn.show()

                #sys.exit(0)
        if not otherusersalive:
            if not self.mpStatus:
                self.checkThreadTimerbot.stop()
            self.checkThreadTimerVictory.stop()
            self.checkThreadTimerSB.stop()
            self.statusBar().showMessage("Vous venez de gagner la partie !!!!")
            victory=QPixmap("./assets/img/menu/victory.png")
            uwin=QLabel(self)
            uwin.move(self.width()/2-1156/2,self.height()/2-594/2-12)
            uwin.setFixedSize(1156,594)
            uwin.setPixmap(victory)
            uwin.show()
            quitbtn=QPushButton(self)
            quitbtn.setObjectName("quitbtn")
            quitbtn.setFixedSize(213,56)
            quitbtn.setStyleSheet("#quitbtn { border-image: url(./assets/img/bg/quit_v.png);} #quitbtn:hover { border-image: url(./assets/img/bg/quit.png);}")
            quitbtn.move(self.width()*0.415234375,self.height()*0.811111111)
            if self.mpStatus:
                quitbtn.clicked.connect(self.disconnect)
            else:
                quitbtn.clicked.connect(self.quit)
            
            quitbtn.show()




            #infobox = QMessageBox.information(self,"Félicitations!","Vous venez de gagner la partie !",QMessageBox.Ok)




    def disablebomb(self):
        self.getMap()
        if len(self.posbbexp)>0:
            for i in self.posbbexp[0]:
                self.carte[i[0]][i[1]]=" "
            self.posbbexp.remove(self.posbbexp[0])
        self.drawNewMap()
        self.activebombe.stop()




    def bougeplayer(self):
        if len(self.bb)>0:
            if self.bb[0][1]+3<time.time():
                #print("La bombe va exploser maintenant !")
                infobombe=self.bb.pop(0)
                mynewcontent,tmp=moveapi.explosionbombe(self.carte,infobombe[0])
                self.posbbexp.append(tmp)
                self.carte=mynewcontent
                self.mabombe=False
                self.activebombe.start()
                self.drawNewMap()
    
    def disableCd(self):
        self.itembarrmv.setPixmap(self.nonrmv[0])
        self.itembarrmv.setToolTip(self.nonrmv[1])
        self.bombCdDisabled=False
        self.bombCd.stop()

    def chkfabien(self):

        if len(self.fabien) == 0:
            self.checkThreadTimerFAB.stop()
            self.drawNewMap()
        else:
            act=moveapi.elevage_de_moi(self.carte,self.playerId,self.fab_act)
            self.carte=act[0]
            self.fab_act=act[1]
            self.fabien=act[2]


    def bougebot(self):
        choixdeplacement = random.randint(0,4)
        if choixdeplacement == 0:
            self.getMap()
            self.carte, rien=moveapi.moveleft(self.carte,"2",[])
            if moveapi.positionblock("2",self.carte):
                zz=moveapi.posebombe("2",self.carte)
                #self.carte=zz[0]
                self.bb.append([zz[1],time.time(),False])
                self.drawNewMap()
                self.bombeposee=[True,time.time()]
                self.botbb=True
            self.drawNewMap()

        elif choixdeplacement == 1:
            self.getMap()
            self.carte, rien=moveapi.moveright(self.carte,"2",[])
            if moveapi.positionblock("2",self.carte):
                zz=moveapi.posebombe("2",self.carte)
                #self.carte=zz[0]
                self.bb.append([zz[1],time.time(),False])
                self.drawNewMap()
                self.bombeposee=[True,time.time()]
            self.drawNewMap()

        elif choixdeplacement == 2:
            self.getMap()
            self.carte, rien=moveapi.moveup(self.carte,"2",[])
            if moveapi.positionblock("2",self.carte):
                zz=moveapi.posebombe("2",self.carte)
                #self.carte=zz[0]
                self.bb.append([zz[1],time.time()])
                self.drawNewMap()
                self.bombeposee=[True,time.time()]
            self.drawNewMap()

        elif choixdeplacement == 3:
            self.getMap()
            self.carte, rien=moveapi.movedown(self.carte,"2",[])
            if moveapi.positionblock("2",self.carte):
                zz=moveapi.posebombe("2",self.carte)
                #self.carte=zz[0]
                self.bb.append([zz[1],time.time(),False])
                self.drawNewMap()
                self.bombeposee=[True,time.time()]
            self.drawNewMap()





    def getMap(self):
        try:
            self.carte=self.renderArea.getMapStatus()
        except:
            print("echec de récupération de la carte")


    def drawNewMap(self,dl=False):
        if self.mpStatus:
            #e=open("file"+str(self.playerId)+".txt","w")
            #e.write(str(self.carte))
            #e.close()
            if not dl:
                self.senfUpdMap(self.carte)
        self.renderArea.redrawmap(self.carte,self.bb)

    def setZoneJeu(self):
        self.renderArea = RenderArea(self.carte)
        self.setCentralWidget(self.renderArea)



    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class RenderArea(QWidget):
    # RENDER AREA == > ZONE DE JEU

    def __init__(self,mape, parent=None):
        self.parent=parent
        super(RenderArea,self).__init__(parent)
        print("Initialisation de la zone de jeu ...")
        # Mise de la carte en variable locale du renderarea
        self.map=mape
        # Mise en cache des blocks par rapport à leur image
        self.unbreakable=QImage("./assets/img/blocks/unbreak1.png")
        self.breakable=QImage("./assets/img/blocks/sinvader.png")
        self.player=QImage("./assets/img/players/player1/up1.png")
        self.fabien=QImage("./assets/img/blocks/fabien.png")
        self.bg=QImage("./assets/img/bg/stars.png")
        self.bomb=QImage("./assets/img/blocks/nw_bomb.gif")
        self.explode=QImage("./assets/img/blocks/Explosion.png")
        self.itm_fabien=QImage("./assets/img/blocks/itm_fabien.png")
        self.itm_rmv=QImage("./assets/img/blocks/itm_rmv.png")
        self.itm_nuke=QImage("./assets/img/blocks/itm_nuke.png")
        self.Onuke=QImage("./assets/img/blocks/nuke.png")
        # Mise des bombes a vide au démarrage
        self.bpos=[]


    def getMapStatus(self):
        # Retourne la carte dessinée au jeu
        return self.map

    # Fonction de redessin de la carte
    def redrawmap(self,carte,bpos):
        # affectation des paramètres
        self.bpos=bpos
        # mise à jour de la carte visuellement
        self.update()
        self.oldmap=carte
        self.map=carte


    def paintEvent(self, event):
        # mise en cache de la carte actuelle
        self.oldmap=self.map
        # lancement du QPainter pour redessiner l'élèment
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QBrush(QColor(255,255,255)))
        # Affectation de la taille de la zone de dessin (1156 * 594)
        r1=QRect((self.width()-1156)/2,(self.height()-594)/2,1156,594)
        # Dessin du background
        painter.drawImage(r1,self.bg)
        emplacementX=(self.width()-1156)/2
        emplacementY=(self.height()-594)/2
        painter.setPen(QColor(0,0,0,0))
        for i in range(0,len(self.map)):
            for n in range(0,len(self.map[i])):
                # Pour chaque case de la carte, on récupère son contenu
                j=self.map[i][n]
                # on définit là ou est le carré
                rect=QRect(emplacementX,emplacementY,89,54)
                # Pour chaque cas ...
                if j == "X": # X correspond à un block incassable
                    painter.setBrush(QBrush(QColor(0,0,0)))
                    painter.drawImage(rect,self.unbreakable)
                elif j ==  "o": # o correspond à un block cassable
                    painter.setBrush(QBrush(QColor(140, 98, 0)))
                    painter.drawImage(rect,self.breakable)
                elif j == "ifb": # ifb correspond à l'item attaque de fabien
                    painter.setBrush(QBrush(QColor(140, 98, 0)))
                    painter.drawImage(rect,self.itm_fabien)
                elif j == "rmv": # rmv correspond à l'item de suppression du timeout de bombe
                    painter.setBrush(QBrush(QColor(140, 98, 0)))
                    painter.drawImage(rect,self.itm_rmv)
                elif j == "nk": # nk correspond à l'item de la bombe nucléaire
                    painter.setBrush(QBrush(QColor(140, 98, 0)))
                    painter.drawImage(rect,self.itm_nuke)
                elif j == " ": # si la zone est vide
                    # On vérifie alors si ce n'est pas une bombe normale ou une bombe nucléaire (car stockée à un endroit différent)
                    nope=True
                    if len(self.bpos)>0:
                        for u in self.bpos:
                            if u[0][0] == i and u[0][1]==n:
                                if len(u)>2:
                                    if u[2]:
                                        nuke=True
                                    else:
                                        nuke=False
                                nope=False
                    # si ce n'est ni une bombe, ni une nuke
                    if nope:
                        # on dessine une zone vide (avec le rgba)
                        painter.setBrush(QBrush(QColor(255,255,255,0)))
                        painter.drawRect(rect)
                    elif nuke:
                        painter.setBrush(QBrush(QColor(255, 255, 0)))
                        painter.drawImage(rect,self.Onuke)
                    else:
                        painter.setBrush(QBrush(QColor(255, 255, 0)))
                        painter.drawImage(rect,self.bomb)


                elif j == "f": # f correspond à fabien
                    painter.setBrush(QBrush(QColor(255, 255, 0)))
                    painter.drawImage(rect,self.fabien)
                # ex correspond à des effets d'explosion
                elif j == "ex":
                    painter.setBrush(QBrush(QColor(255, 255, 0)))
                    painter.drawImage(rect,self.explode)

                else:
                    # si c'est un joueur
                    painter.setBrush(QBrush(QColor(255,255,255,0)))
                    painter.drawImage(rect,self.player)


                emplacementX+=89
            emplacementX=(self.width()-1156)/2
            emplacementY+=54

        # on coupe le painter
        painter.end()


# Fonction créant la carte
def createGameMap():
    carte=[]
    for i in range(0,11):
        carte.append([])
        for j in range(0,13):
            if i % 2 != 0 and j % 2 != 0:
                carte[i].append("X")
            else:
                carte[i].append(" ")
    for i in range(0,len(carte)):
        for j in range(0,len(carte[i])):
            rdm=random.randint(0,1)
            if rdm == 1 and carte[i][j] != "X":
                carte[i][j]="o"

    return carte


# préparation de la carte par rapport au nombre de joueurs
def prepareGame(joueurs,carte,multi):
    for i in range(0,joueurs):
        if i == 0:
            carte[0][0]=str(i+1)
            carte[0][1]=" "
            carte[1][0]=" "
        elif i == 1:
            #if not multi:
            carte[0][len(carte[0])-1]=str(i+1)
            #else:
            #    carte[0][len(carte[0])-1]=" "
            carte[0][len(carte[0])-2]=" "
            carte[1][len(carte[0])-1]=" "
        elif i == 2:
            #if not multi:
            carte[len(carte)-1][0]=str(i+1)
            #else:
            #    carte[len(carte)-1][0]=" "
            carte[len(carte)-2][0]=" "
            carte[len(carte)-1][1]=" "
        elif i == 3:
            #if not multi:
            carte[len(carte)-1][len(carte[0])-1]=str(i+1)
            #else:
            #    carte[len(carte)-1][len(carte[0])-1]=" "
            carte[len(carte)-2][len(carte[0])-1]=" "
            carte[len(carte)-1][len(carte[0])-2]=" "
    return carte

def getPos(joueur,carte):
    for i in range(0,len(carte)):
        for j in range(0,len(carte[i])):
            if carte[i][j]==joueur:
                return [i,j]
    return [-1,-1]

def explosionbombe(carte,joueur):
    positionJ=getPos(joueur,carte)


app = Application([])
win = Window()
app.exec_()
