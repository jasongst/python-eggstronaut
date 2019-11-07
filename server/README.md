# LE SERVEUR

Vous êtes sur la partie serveur du jeu. Afin de pouvoir l'installer chez vous, vous devez disposer sur votre machine (ou une autre) d'apache2 (ou autre serveur sachant éxectuer le PHP)
Vous devez également avoir sur cette machine un serveur MySQL pour stocker la base de donnée des parties.

## Tutorial d'installation :

**Il faut que vous soyez root pour suivre la procédure linux**
**Pas besoin de l'être avec XAMPP sur windows**

- pour installer les élèments requis sur linux :
    `sudo apt install apache2 mysql-server phpmyadmin`
- configurer le serveur:
    - tout d'abord récupérez le fichier .sql de la structure de la base de donnée sur ce dépot
    - accédez sur votre *serveur* à phpmyadmin (typiquement [http://localhost/phpmyadmin](http://localhost/phpmyadmin)).
    - ensuite crééz une base de donnée et allez ensuite dans importer en entrant le fichier .sql

- importer l'api
    - récupérez le fichier PHP sur ce dépot
    - vous allez devoir créer plusieurs répertoire dans le /var/www/html/, qui est 1iut/tutoreS2/ : `cd /var/www/html && mkdir ./1iut && mkdir ./1iut/tutoreS2`
    - placez le fichier php dans ce nouveau dossier : `cp requests.php /var/www/html/1iut/tutoreS2/`
    
    - il faudra modifier le fichier html:
        ```
        $user="username"; // remplacez ici username par votre nom d'utilisateur de base de données
        $pass="password"; // remplacez par votre mot de passe
        $dbname="database"; // remplacez par le nom de votre base de données
        ```

## Utilisation :

Pour utiliser un serveur privé, il faut sur le menu du jeu appuyer sur la touche CTRL.
Une fenêtre va apparaître pour demander une adresse, entrez celle de votre serveur
Puis appuyez sur OK et le tour est joué.

*par contre, le serveur que vous avez séléctionné n'est pas enregistré pour la session suivante !!!*
