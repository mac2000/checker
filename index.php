<?php
require_once 'config.php';
require_once 'lib/rb.php';
require_once 'vendor/autoload.php';

R::setup('mysql:host=' . DBHOST . ';dbname=' . DBNAME, DBUSER, DBPASS);

$requiredAuth = function (\Slim\Route $route) {
    $app = \Slim\Slim::getInstance();
    $user =  $app->getEncryptedCookie('user');
    if(!$user) {
        $app->deleteCookie('user');
        $app->flash('error', 'Auth required');
        $app->redirect($app->urlFor('login'));
    }
};

// Prepare app
$app = new \Mac\Slim(array(
    'templates.path' => 'templates',
    'cookies.secret_key' => DBPASS,
    /*'log.level' => 4,
    'log.enabled' => true,
    'log.writer' => new \Slim\Extras\Log\DateTimeFileWriter(array(
        'path' => '../logs',
        'name_format' => 'y-m-d'
    ))*/
));

$app->hook('slim.before', function() use($app) {
    $user = $app->getEncryptedCookie('user');
    $app->view()->appendData(array(
        'base' => $app->urlFor('home'),
        'user' => $user
    ));
});

$app->hook('slim.after.router', function() use($app) {
    $app->view()->appendData(array(
        'name' => $app->router()->getCurrentRoute()->getName()
    ));
});

\Slim\Route::setDefaultConditions(array(
    'id' => '\d+'
));

// Prepare view
\Slim\Extras\Views\Twig::$twigOptions = array(
    'charset' => 'utf-8',
    'cache' =>  'templates/cache',
    'auto_reload' => true,
    'strict_variables' => false,
    'autoescape' => true
);
\Slim\Extras\Views\Twig::$twigExtensions = array(
    'Twig_Extensions_Slim',
);
$app->view(new \Slim\Extras\Views\Twig());

// Define routes
$app->get('/', $requiredAuth, function () use ($app) {
    $app->render('index.html');
})->name('home');

require_once 'routes/auth.php';
require_once 'routes/users.php';

// Run app
$app->run();