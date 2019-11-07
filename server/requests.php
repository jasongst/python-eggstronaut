<?php
$user="username";
$pass="password";
$dbname="database";
try {
    $dbh = new PDO('mysql:host=localhost;dbname='.$dbname, $user, $pass);
} catch (PDOException $e) {
    print "Erreur !: " . $e->getMessage() . "<br/>";
    die();
}

function createGame($map,$bd,$data) {
    try {
    $sql="SELECT MAX(ident_partie) AS maximum FROM parties";
    foreach  ($bd->query($sql) as $row) {
        $max= $row['maximum'];
    }
    $mapartieid=$max+1;
    $req = $bd->prepare("INSERT INTO parties (ident_partie, nbjoueurs, posjrs) VALUES (:ident_partie,:nbjrs,:posjrs)");
    $req->execute(array(
            "ident_partie" => $mapartieid, 
            "nbjrs" => 1,
            "posjrs" => $data
            ));
    echo '{"OK":"OK","id_partie":'.$mapartieid."}";
} catch(PDOException $e) {
    echo json_encode(["error"=>"Impossible de créer la partie, une erreur serveur est survenue !"]);
}
}

function returnversionserver() {
    $game_ver="1.0.6";
    $json = ["server_version"=>$game_ver,"conn_state"=>"OK"];
    echo json_encode($json);
}

function ajouteunp($idP,$dbh) {
    $sql="SELECT nbjoueurs AS nbj FROM parties WHERE ident_partie=$idP";
    try {
        foreach($dbh->query($sql) as $row) {
            $nbj=$row["nbj"];
        }
        if($nbj=="") {
            echo '{"error":"La partie est inexistante ou celle ci a été fermée !"}';
        } else {
            echo $data;
            $nbj++;
        $req=$dbh->prepare("UPDATE parties SET nbjoueurs = :nbj WHERE ident_partie=$idP");
        $req->execute(array("nbj"=>$nbj));
        echo '{"player_id":'.$nbj.'}';
        }
        

    
    
    } catch(PDOException $e){
        echo json_encode(["error"=>"Impossible de créer la partie, une erreur serveur est survenue !"]);
    }
}


function returngamedata($dbh,$idP) {
    $sql="SELECT posjrs FROM parties WHERE ident_partie=$idP";
    try {
        foreach($dbh->query($sql) as $row) {
            $data=$row["posjrs"];
        }
        if($data=="") {
            echo '{"error":"La partie est inexistante ou celle ci a été fermée !"}';
        } else {
            echo $data;
        }
    } catch(PDOException $e){
        echo json_encode(["error"=>"Impossible de créer la partie, une erreur serveur est survenue !"]);
    }
}

function updatemap($dbh,$idP,$data) {
    try {
    $req = $dbh->prepare("UPDATE parties SET posjrs=:party WHERE ident_partie=$idP");
    $req->execute(array(
        "party" => $data
        ));
    echo '{"OK":"OK"}';
    
} catch(PDOException $e) {
    echo json_encode(["error"=>"Impossible de mettre à jour la partie, peut-être que celle ci n'existe plus !"]);
}


}


function deletegame($idP,$dbh) {
    try {
        $sql = "DELETE FROM parties WHERE ident_partie=$idP";
        $dbh->query($sql);
        echo '{"OK":"La Partie a été supprimée"}';
    } catch(PDOException $e) {
        echo json_encode(["error"=>"Impossible de supprimer la partie !"]);
    }
}

if (isset($dbh)) {
    if (isset($_GET['act'])) {
        switch($_GET['act']){
            case "creategame":
                if(isset($_POST['data'])) {
                createGame("ccc",$dbh,$_POST['data']);
                } else {
                    echo '{"error":"Aucune donnee recue !"}';  
                }
                break;
            case "getmap":
                if(isset($_GET['idP'])) {
                    returngamedata($dbh,$_GET['idP']);
                } else {
                    echo '{"error":"Aucune partie a été selectionée !"}';
                }
                break;
            case "getver":
                returnversionserver();
                break;
            case "updmap":
                if(isset($_GET['idP']) && isset($_POST['data'])) {
                    updatemap($dbh,$_GET['idP'],$_POST['data']);
                } else {
                    echo '{"error":"Aucune partie a été selectionée, ou bien que les donnees ne sont pas specifiees !"}';
                }
                break;
            case "deletegame":
                if(isset($_GET['idP'])) {
                    deletegame($_GET['idP'],$dbh);
                }else {
                    echo '{"error":"Aucune partie a été selectionée"}';
                }
                break;
            case "addplayer":
            if(isset($_GET['idP'])) {
                ajouteunp($_GET['idP'],$dbh);
            }else {
                echo '{"error":"Aucune partie a été selectionée"}';
            }
        }
    }
}




?>