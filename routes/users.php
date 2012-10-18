<?php
$app->get('/users', $requiredAuth, function () use ($app) {
    $app->render('users.html', array(
        'users' =>  R::findAll('user', ' ORDER BY username')
    ));
})->name('users');

$app->post('/users', $requiredAuth, function () use ($app) {
    $username = $app->request()->post('username');
    $password = $app->request()->post('password');
    $hash = md5(DBPASS . md5(DBPASS . $password));
    $user = R::findOne('user', 'username=:username', array(':username' => $username));
    if(empty($username) || empty($password)) {
        $app->flashNow('error', 'Both fields are required');
        $app->render('users.html', array(
            'username' => $username,
            'password' => $password,
            'users' =>  R::findAll('user', ' ORDER BY username')
        ));
    }
    else if($user) {
        $app->flashNow('error', 'User already exists');
        $app->render('users.html', array(
            'username' => $username,
            'password' => $password,
            'users' =>  R::findAll('user', ' ORDER BY username')
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

$app->post('/users/change/password', $requiredAuth, function () use ($app) {
    $current_user = $app->getEncryptedCookie('user');
    $id = $app->request()->post('id');
    $password = $app->request()->post('password');
    $hash = md5(DBPASS . md5(DBPASS . $password));

    $user = R::load('user', $id);
    if(!$user) {
        $app->flash('error', "user not found");
        $app->redirect($app->urlFor('users'));
    }
    else {
        $user->password = $hash;
        R::store($user);

        if($current_user == $user->username) {
            $app->deleteCookie('user');
        }
        $app->flash('success', "user password changed");
        $app->redirect($app->urlFor('users'));
    }
})->name('users_change_password');

$app->get('/users/:id/delete', $requiredAuth, function ($id) use ($app) {
    $current_user = $app->getEncryptedCookie('user');
    $user = R::load('user', $id);
    if(!$user) {
        $app->flash('error', "user not found");
        $app->redirect($app->urlFor('users'));
    }
    else {
        if($current_user == $user->username) {
            $app->deleteCookie('user');
        }

        R::trash($user);
        $app->flash('success', $user->username . " deleted");
        $app->redirect($app->urlFor('users'));
    }
})->name('users_delete');