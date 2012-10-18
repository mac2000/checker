<?php
$app->get('/proxies', $requiredAuth, function () use ($app) {
    $app->render('proxies.html', array(
        'proxies' =>  R::findAll('proxy', ' ORDER BY host')
    ));
})->name('proxies');

$app->post('/proxies', $requiredAuth, function () use ($app) {
    $url = $app->request()->post('url');
    $username = $app->request()->post('username');
    $password = $app->request()->post('password');
    $port = $app->request()->post('port');

    $host = parse_url($url, PHP_URL_HOST);

    $proxy = R::findOne('proxy', 'host=:host', array(':host' => $host));

    if(empty($host) || empty($username) || empty($password) || empty($port)) {
        $app->flashNow('error', 'Fields are required');
        $app->render('proxies.html', array(
            'url' => $url,
            'username' => $username,
            'password' => $password,
            'port' => $port,
            'proxies' =>  R::findAll('proxy', ' ORDER BY host')
        ));
    }
    else if($proxy) {
        $app->flashNow('error', 'proxy already exists');
        $app->render('proxies.html', array(
            'proxy' => $url,
            'username' => $username,
            'password' => $password,
            'port' => $port,
            'proxies' =>  R::findAll('proxy', ' ORDER BY host')
        ));
    }
    else {
        $proxy = R::dispense('proxy');
        $proxy->host = $host;
        $proxy->username = $username;
        $proxy->password = $password;
        $proxy->port = $port;
        $id = R::store($proxy);

        $app->flash('success', "$host created");
        $app->redirect($app->urlFor('proxies'));
    }
});

$app->get('/proxies/:id/delete', $requiredAuth, function ($id) use ($app) {
    $proxy = R::load('proxy', $id);
    if(!$proxy) {
        $app->flash('error', "proxy not found");
        $app->redirect($app->urlFor('proxies'));
    }
    else {
        R::trash($proxy);
        $app->flash('success', $proxy->host . " deleted");
        $app->redirect($app->urlFor('proxies'));
    }
});