<?php
$app->get('/users', $requiredAuth, function () use ($app) {
    $app->render('users.html', array(
        'users' =>  R::findAll('user', ' ORDER BY username')
    ));
})->name('users');

$app->get('/users/add', $requiredAuth, function () use ($app) {
    $app->render('users/add.html');
})->name('users_add');

$app->post('/users/add', $requiredAuth, function () use ($app) {
    $username = $app->request()->post('username');
    $password = $app->request()->post('password');
    $hash = md5(DBPASS . md5(DBPASS . $password));
    $user = R::findOne('user', 'username=:username', array(':username' => $username));
    if(empty($username) || empty($password)) {
        $app->flashNow('error', 'Both fields are required');
        $app->render('users/add.html', array(
            'username' => $username,
            'password' => $password
        ));
    }
    else if($user) {
        $app->flashNow('error', 'User already exists');
        $app->render('users/add.html', array(
            'username' => $username,
            'password' => $password
        ));
    }
    else {
        $user = R::dispense('user');
        $user->username = $username;
        $user->password = $hash;
        $id = R::store($user);
        $app->flash('success', "$username created");
        $app->redirect($app->urlFor('users'));
    }
});