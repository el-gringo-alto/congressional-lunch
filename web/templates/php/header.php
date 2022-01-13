<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php if ($description == null) {
        $description = "A Twitter feed generated through machine learning using tweets from a congressman's own party.";
    } ?>
    <meta name="description" content="<?=$description?>">
    <meta name="author" content="Sam Schultheis">
    <?php
        if ($title != null) {
            $title .= ' | ';
        } else {
            $title = '';
        }
        $title .= 'Congressional Lunch';
    ?>
    <title><?=$title?></title>
    <!-- facebook and twitter card meta tags -->
    <meta name="twitter:card" content="summary">
    <meta property="og:title" content="<?=$title?>">
    <meta property="og:description" content="<?=$description?>">
    <?php if ($og_img == null) {
        $og_img = "http://congressional-lunch.com/assets/imgs/congressional-lunch-logo-card.png";
    } ?>
    <meta property="og:image" content="<?=$og_img?>">
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JHEPND2F62"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-JHEPND2F62');
    </script>
    <link rel="stylesheet" href="assets/css/master.css">
    <link rel="stylesheet" href="assets/css/temp.css">
    <script src="assets/js/script.js"></script>
    <script src="https://kit.fontawesome.com/0fd958d790.js" crossorigin="anonymous"></script>
</head>
<body class="<?php
    if (strtolower($_GET['header']) != 'false') {
        echo 'header-visible';
    } else {
        echo 'header-invisible';
    }
?>">
    <?php if (strtolower($_GET['header']) != 'false'): ?>
        <header class="header-container">
            <a class="logo" href="/index.php"><img src="assets/imgs/congressional-lunch-logo.svg" alt="Congressional Lunch logo"></a>
            <div id="main-nav" class="main-nav">
                <a class="btn-nav" href="/about.php">About</a>
                <a class="btn-nav" href="/random.php">Random Tweet</a>
            </div>
            <div class="disclaimer">
                <p>Congressional Lunch is a parody social media website that attributes fake posts to real people in a fictitious manner. All posts within congressional-lunch.com are fake and do not represent the opinions of those that they are attributed to.</p>
                <p>&copy; <?=date('Y')?> Sam Schultheis</p>
            </div>
        </header>
    <?php endif; ?>
    <main id="main-content">
