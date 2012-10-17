<?php
namespace Mac;

class Slim extends \Slim\Slim
{
    public function __construct($userSettings = array()) {
        parent::__construct($userSettings);

        //$this->dbh = new PDO('mysql:host=localhost;dbname=auth', 'root', '5340940'); //TODO: extract me
        //$this->dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    /*
    public function all($sql, $params = array()) {
        $stmt = $this->dbh->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_OBJ);
    }
    public function one($sql, $params = array()) {
        $stmt = $this->dbh->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetch(PDO::FETCH_OBJ);
    }
    public function execute($sql, $params = array()) {
        $stmt = $this->dbh->prepare($sql);
        $stmt->execute($params);
        if(preg_match('/insert/i', $sql)) return $this->dbh->lastInsertId();
        else return $stmt->rowCount();
    }
     */
}
