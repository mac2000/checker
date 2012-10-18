<?php
$app->get('/keywords', $requiredAuth, function () use ($app) {
    $app->render('keywords.html', array(
        'keywords' =>  R::findAll('keyword', ' ORDER BY keyword')
    ));
})->name('keywords');

$app->post('/keywords', $requiredAuth, function () use ($app) {
    $word = $app->request()->post('keyword');

    $keyword = R::findOne('keyword', 'keyword=:keyword', array(':keyword' => $word));

    if(empty($word)) {
        $app->flashNow('error', 'Fields are required');
        $app->render('keywords.html', array(
            'keyword' => $word,
            'keywords' =>  R::findAll('keyword', ' ORDER BY keyword')
        ));
    }
    else if($keyword) {
        $app->flashNow('error', 'Keyword already exists');
        $app->render('keywords.html', array(
            'keyword' => $word,
            'keywords' =>  R::findAll('keyword', ' ORDER BY keyword')
        ));
    }
    else {
        $keyword = R::dispense('keyword');
        $keyword->keyword = $word;
        $id = R::store($keyword);
        $app->flash('success', "$word created");
        $app->redirect($app->urlFor('keywords'));
    }
});

$app->get('/keywords/:id/delete', $requiredAuth, function ($id) use ($app) {
    $keyword = R::load('keyword', $id);
    if(!$keyword) {
        $app->flash('error', "keyword not found");
        $app->redirect($app->urlFor('keywords'));
    }
    else {
        R::trash($keyword);
        $app->flash('success', $keyword->keyword . " deleted");
        $app->redirect($app->urlFor('keywords'));
    }
});