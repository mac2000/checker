<?php
$app->get('/domains', $requiredAuth, function () use ($app) {
    $app->render('domains.html', array(
        'domains' =>  R::findAll('domain', ' ORDER BY host')
    ));
})->name('domains');

$app->post('/domains', $requiredAuth, function () use ($app) {
    $url = $app->request()->post('url');
    $host = parse_url($url, PHP_URL_HOST);

    $domain = R::findOne('domain', 'host=:host', array(':host' => $host));

    if(empty($host)) {
        $app->flashNow('error', 'Fields are required');
        $app->render('domains.html', array(
            'url' => $url,
            'domains' =>  R::findAll('domain', ' ORDER BY host')
        ));
    }
    else if($domain) {
        $app->flashNow('error', 'domain already exists');
        $app->render('domains.html', array(
            'url' => $url,
            'domains' =>  R::findAll('domain', ' ORDER BY host')
        ));
    }
    else {
        $domain = R::dispense('domain');
        $domain->host = $host;
        $id = R::store($domain);
        //TODO: add job for domain here
        $app->flash('success', "$host created");
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
        $app->flash('success', $domain->host . " deleted");
        $app->redirect($app->urlFor('domains'));
    }
});