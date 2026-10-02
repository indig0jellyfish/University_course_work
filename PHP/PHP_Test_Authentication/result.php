<?php

require_once __DIR__ . '/includes/functions.php';

$email = $_GET['email'] ?? '';
$score = isset($_GET['score']) ? (int) $_GET['score'] : null;

if ($email === '' || $score === null || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: index.php');
    exit;
}

$questions = getQuestions();
$maxScore = count($questions);
$average = getAverageScore();

if ($score > $average) {
    $comparison = 'Sunteti foarte bravo - faceti parte din chestionatii care au un punctaj peste medie!';
    $cssClass = 'above';
} elseif ($score < $average) {
    $comparison = 'Punctajul dvs. este sub media generala. Mai multa atentie la urmatoarea tentativa!';
    $cssClass = 'below';
} else {
    $comparison = 'Punctajul dvs. este exact egal cu media generala.';
    $cssClass = 'equal';
}
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Rezultatul testului</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Rezultatul testului</h1>
        <p>Email: <strong><?php echo h($email) ?></strong></p>

        <div class="result-box">
            <p>Punctajul dvs.: <strong><?php echo (int) $score ?> / <?php echo (int) $maxScore ?></strong></p>
            <p>Media generala a tuturor utilizatorilor: <strong><?php echo number_format($average, 2) ?> / <?php echo (int) $maxScore ?></strong></p>
            <p class="comparison <?php echo h($cssClass) ?>"><?php echo h($comparison) ?></p>
        </div>

        <a class="btn" href="index.php">Inapoi la pagina de start</a>
    </div>
</body>
</html>
