<!doctype html>
<title>tmp</title>
<meta charset="utf-8">
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/twitter-bootstrap/latest/css/bootstrap-combined.min.css">
<div class="container-fluid" style="padding:20px">
    <?php
        $config = parse_ini_file('config.ini', true);
        $dbh = new PDO('mysql:host=' . $config['mysql']['host'] . ';dbname=' . $config['mysql']['db'], $config['mysql']['user'], $config['mysql']['pass']);
    ?>

    <h3>Today</h3>
    <p>Total records: <?php echo $dbh->query("select count(*) as total from cron where `date` = date(now());")->fetchColumn(0);?></p>
    <p>Keywords: <?php echo $dbh->query("select count(*) from (select distinct keyword from cron where `date` = date(now())) as k;")->fetchColumn(0);?></p>

    <table class="table">
        <thead>
            <tr><th>keyword</th><th>total</th></tr>
        </thead>
        <tbody>
    <?php
        foreach ($dbh->query("select keyword, count(*) as total from cron where `date` = date(now()) group by keyword order by keyword;") as $row) {
            echo '<tr><td>' . $row['keyword'] . '</td><td>' . $row['total'] . '</td></tr>';
        }
    ?>
    </tbody>
    </table>

    <h3>Dates</h3>
    <table class="table">
        <thead>
            <tr><th>date</th><th>total</th></tr>
        </thead>
        <tbody>
    <?php
        foreach ($dbh->query("select `date`, count(*) as total from cron group by `date` order by `date`;") as $row) {
            echo '<tr><td>' . $row['date'] . '</td><td>' . $row['total'] . '</td></tr>';
        }
    ?>
    </tbody>
    </table>


    <h3>Yesterday</h3>
    <p>Total records: <?php echo $dbh->query("select count(*) as total from cron where `date` = subdate(current_date, 1);")->fetchColumn(0);?></p>
    <p>Keywords: <?php echo $dbh->query("select count(*) from (select distinct keyword from cron where `date` = subdate(current_date, 1)) as k;")->fetchColumn(0);?></p>

    <table class="table">
        <thead>
            <tr><th>keyword</th><th>total</th></tr>
        </thead>
        <tbody>
    <?php
        foreach ($dbh->query("select keyword, count(*) as total from cron where `date` = subdate(current_date, 1) group by keyword order by keyword;") as $row) {
            echo '<tr><td>' . $row['keyword'] . '</td><td>' . $row['total'] . '</td></tr>';
        }
    ?>
    </tbody>
    </table>



    <h3>Log</h3>
    <table class="table">
        <thead>
            <tr><th>date</th><th>keyword</th><th>position</th><th>domain</th></tr>
        </thead>
        <tbody>
    <?php
        foreach ($dbh->query("SELECT date,keyword,position,domain FROM cron LIMIT 100") as $row) {
            echo '<tr><td>' . $row['date'] . '</td><td>' . $row['keyword'] . '</td><td>' . $row['position'] . '</td><td>' . $row['domain'] . '</td></tr>';
        }
    ?>
    </tbody>
    </table>
</div>
