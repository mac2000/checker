<?php
require_once 'inc.php';
$t = microtime(true);

// READ CONFIG
$config = parse_ini_file('config.ini', true);

// COMMAND LINE ARGUMENTS
extract(getopt('k:l:c:p:', array('keyword:', 'language:', 'country:', 'proxy:', 'nodb')));

$keyword = isset($keyword) ? $keyword : (isset($k) ? $k : '');
$language = isset($language) ? $language : (isset($l) ? $l : 'lang_en');
$country = isset($country) ? $country : (isset($c) ? $c : 'countryUS');
$proxy = isset($proxy) ? $proxy : (isset($p) ? $p : false);
$nodb = isset($nodb);

// CHECK THAT KEYWORD IS GIVEN
if(empty($keyword)) die('Usage: php cron.php -k <keyword> [-l <language>] [-c <country>] [-p http://<user>:<pass>@<host>:<port>]');

// CHECK THAT GIVEN PROXY IS GOOD
if($proxy) {
    extract(parse_url($proxy));
    if(empty($user) || empty($pass) || empty($host) || empty($port)) die('Wrong proxy given');

    $response = get_html('http://checker.mac-blog.org.ua/ip.php', null, null, null, $host, $port, $user, $pass);

    if($response['http_code'] != 200 || trim($response['body']) != trim($host)) die('Bad response from given proxy');
} else {
    $user = null;
    $pass = null;
    $host = null;
    $port = null;
}

// USER AGENTS
$useragents = explode(PHP_EOL, file_get_contents('useragents.txt'));
shuffle($useragents);
$useragent = trim(array_shift($useragents));

// COOKIE FILE
$cookie = tempnam(sys_get_temp_dir(), 'cookie');

// XPATH
$xpath_query = trim(file_get_contents('xpath.txt'));

// STEP 1. GO TO GOOGLE
$responses = array();
$url = 'http://www.google.com/';
$response = get_html($url, $useragent, $cookie, null, $host, $port, $user, $pass);
sleep(1);
if($response['http_code'] == 200) {

    // STEP 2. GO THROUGHT 10 SEARCH RESULTS
    for($page = 1; $page <= 10; $page++) {
        $referrer = $url;
        $url = 'http://www.google.com/search?q=' . urlencode($keyword) . '&hl=en&lr=' . $language . '&cr=' . $country;
        if($page > 1) $url = $url . '&start=' . (($page - 1) * 10);

        $response = get_html($url, $useragent, $cookie, $referrer, $host, $port, $user, $pass);
        echo '[' . ($response['http_code'] == 200 ? '+' : '-') . '] page: ' . $page . PHP_EOL;
        $responses[] = $response;
        sleep($config['curl']['sleep']);
    }

    // STEP 3. ANALYZE DATA
    $good_responses = array_filter($responses, function($response) { return $response['http_code'] == 200; });
    // STEP 3.1 CHECK FOR CAPTCHA
    if(count($responses) == count(array_filter($responses, function($response) { return $response['http_code'] == 503; }))) {
        die('[!] Captcha detected');
        //TODO: mail here
    } else {
        echo '[*] Done in ' . round(microtime(true) - $t) . ' seconds with ' . count($good_responses) . ' good and ' . (count($responses) - count($good_responses)) . ' bad responses' . PHP_EOL;

        $links = array();

        // STEP 3.2 PARSE RESPONSES
        foreach($good_responses as $response) {
            $dom = new DOMDocument();
            @$dom->loadHTML($response['body']);
            $dom_xpath = new DOMXPath($dom);
            $dom_nodes = $dom_xpath->query("//li[@class='g' and not(@id)]//h3/a");
            foreach ($dom_nodes as $node) {
                $link = $node->getAttribute('href');
                $links[] = $link;
            }
        }

        if($links < 10 * count($good_responses)) {
            echo '[!] Probably Google HTML changed' . PHP_EOL;
            //TODO: notify
        }

        echo '[*] ' . count($links) . ' links parsed' . PHP_EOL;

        // STEP 3.3 SAVE RESULTS
        $log_dir = 'logs/' . date('Y/m/d') . '/';
        $log_path = $log_dir . sanitize_filename($keyword) . '.json';
        @mkdir($log_dir, 0777, true);
        @file_put_contents($log_path, json_encode($responses));

        try {
            $dbh = new PDO('mysql:host=' . $config['mysql']['host'] . ';dbname=' . $config['mysql']['db'], $config['mysql']['user'], $config['mysql']['pass']);
            $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "INSERT INTO cron VALUES(DATE(NOW()), :keyword, :lr, :cr, :position, :domain, :url) ON DUPLICATE KEY UPDATE domain = :domain, url = :url;";
            $stmt = $dbh->prepare($sql);

            for($i = 0; $i < count($links); $i++) {
                $link = $links[$i];
                if(strpos($link, 'http') === 0) {
                    $domain = parse_url($link, PHP_URL_HOST);
                    $domain = str_replace('www.', '', $domain);
                } else if(strpos($link, '/url?q=http') === 0) {
                    $domain = parse_url($link, PHP_URL_QUERY);
                    parse_str($domain, $output);
                    $domain = $output['q'];
                    $domain = str_replace('www.', '', $domain);
                } else {
                    $domain = 'UNKNOWN';
                }
                if($nodb) {
                    echo '[' . ($i + 1) . '] ' . $domain . PHP_EOL;
                } else {
                    $stmt->execute(array(
                        ':keyword' => $keyword,
                        ':lr' => $language,
                        ':cr' => $country,
                        ':position' => $i + 1,
                        ':domain' => $domain,
                        ':url' => $link
                    ));
                }
            }

            $dbh = null;
        }
        catch(PDOException $e) {
            die($e->getMessage());
        }

    }
} else {
    die("Can not open $url");
}
