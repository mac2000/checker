<?php
$app->get('/domains', $requiredAuth, function () use ($app) {
    $app->render('domains.html', array(
        'domains' =>  R::findAll('domain', ' ORDER BY domain')
    ));
})->name('domains');

$app->post('/domains', $requiredAuth, function () use ($app) {
    $word = $app->request()->post('domain');

    $domain = R::findOne('domain', 'domain=:domain', array(':domain' => $word));

    if(empty($word)) {
        $app->flashNow('error', 'Fields are required');
        $app->render('domains.html', array(
            'domain' => $word,
            'domains' =>  R::findAll('domain', ' ORDER BY domain')
        ));
    }
    else if($domain) {
        $app->flashNow('error', 'domain already exists');
        $app->render('domains.html', array(
            'domain' => $word,
            'domains' =>  R::findAll('domain', ' ORDER BY domain')
        ));
    }
    else {
        $word = parse_URL($word, PHP_URL_HOST);
        $domain = R::dispense('domain');
        $domain->domain = $word;
        $id = R::store($domain);
        $app->flash('success', "$word created");
        $app->redirect($app->urlFor('domains'));
    }
});

$app->get('/domains/:id/delete', $requiredAuth, function ($id) use ($app) {
    $domain = R::load('domain', $id);
    if(!$domain) {
        $app->flash('error', "domain not found");
        $app->redirect($app->urlFor('domains'));
    }
    else {
        R::trash($domain);
        $app->flash('success', $domain->domain . " deleted");
        $app->redirect($app->urlFor('domains'));
    }
});