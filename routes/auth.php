<?php
$app->get('/login', function () use ($app) {
    $app->deleteCookie('user');
    $app->render('login.html');
})->name('login');

$app->post('/login', function () use ($app) {
    $username = $app->request()->post('username');
    $password = $app->request()->post('password');

    if($username == DBUSER && $password == DBPASS) {
        $app->setEncryptedCookie('user', $username);
        $app->redirect($app->urlFor('home'));
    }

    $hash = md5(DBPASS . md5(DBPASS . $password));
    $user = R::findOne('user', 'username=:username AND password=:password', array(':username' => $username, ':password' => $hash));
    if(!$user) {
        $app->deleteCookie('user');
        $app->flashNow('error', 'Wrong email and/or password');
        $app->render('login.html', array(
            'username' => $username,
            'password' => $password
        ));
    } else {
        $app->setEncryptedCookie('user', $username);
        $app->redirect($app->urlFor('home'));
    }
});

$app->get('/logout', function () use ($app) {
    $app->deleteCookie('user');
    $app->redirect('login');
})->name('logout');
