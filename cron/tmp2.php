<!doctype html>
<title>tmp</title>
<meta charset="utf-8">
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/twitter-bootstrap/latest/css/bootstrap-combined.min.css">
<div class="container-fluid" style="padding:20px">
    <?php
        $config = parse_ini_file('config.ini', true);
        $dbh = new PDO('mysql:host=' . $config['mysql']['host'] . ';dbname=' . $config['mysql']['db'], $config['mysql']['user'], $config['mysql']['pass']);
        $keyword = isset($_GET['keyword']) ? $_GET['keyword'] :  false;
        $date = isset($_GET['date']) ? $_GET['date'] :  false;


    ?>

    <form class="form-inline">
        <select name="date">
            <option>date...</option>
            <?php foreach($dbh->query("SELECT DISTINCT `date` FROM cron") as $row):?>
                <option <?php echo $row['date'] == $date ? 'selected="selected"' : "" ?> value="<?php echo $row['date']?>"><?php echo $row['date']?></option>
            <?php endforeach;?>
        </select>

        <select name="keyword">
            <option>keyword...</option>
            <?php foreach($dbh->query("SELECT DISTINCT `keyword` FROM cron") as $row):?>
                <option <?php echo $row['keyword'] == $keyword ? 'selected="selected"' : "" ?> value="<?php echo $row['keyword']?>"><?php echo $row['keyword']?></option>
            <?php endforeach;?>
        </select>

        <input type="submit" value="Filter" class="btn btn-primary">
    </form>

    <?php if($date && $keyword):?>
    <table class="table">
        <?php
        $stmt = $dbh->prepare("SELECT * FROM cron WHERE `date` = :date AND keyword = :keyword");
        $stmt->execute(array('date' => $date, 'keyword' => $keyword));
        while($row = $stmt->fetch()):?>
            <tr>
                <td><?php echo $row['date']?></td>
                <td><?php echo $row['keyword']?></td>
                <td><?php echo $row['position']?></td>
                <td><?php echo $row['domain']?></td>
            </tr>
        <?php endwhile;?>
    </table>

    <?php endif;?>
</div>
