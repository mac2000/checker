<!doctype html>
<title>tmp</title>
<meta charset="utf-8">
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/twitter-bootstrap/latest/css/bootstrap-combined.min.css">
<div class="container-fluid" style="padding:20px">
    <table class="table">
        <thead>
            <tr>
                <th>date</th>
                <th>keyword</th>
                <th>position</th>
                <th>domain</th>
            </tr>
        </thead>
        <tbody>
    <?php
        try {
            $config = parse_ini_file('config.ini', true);

            $dbh = new PDO('mysql:host=' . $config['mysql']['host'] . ';dbname=' . $config['mysql']['db'], $config['mysql']['user'], $config['mysql']['pass']);
            $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "SELECT date,keyword,position,domain FROM cron";

            foreach ($dbh->query($sql) as $row) {
                echo '<tr><td>' . $row['date'] . '</td><td>' . $row['keyword'] . '</td><td>' . $row['position'] . '</td><td>' . $row['domain'] . '</td></tr>';
            }

        }
        catch(Exception $e) {
            die($e->getMessage());
        }

    ?>
    </tbody>
    </table>
</div>
