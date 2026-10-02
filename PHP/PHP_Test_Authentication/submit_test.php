<?php

require_once __DIR__ . '/includes/functions.php'; # imp pentru a folosi functiile

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { # verif daca rasp vin prin post
    header('Location: test.php');
    exit;
}

$errors = validateAnswers($_POST); # se transmit toate datele prin formular

if (!empty($errors)) { # daca exista erori
    ?>
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Erori de validare</title>
        <link rel="stylesheet" href="assets/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Nu am putut prelua testul</h1>
            <ul class="errors">
                <?php foreach ($errors as $error): # se parcurg toate erorile?> 
                    <li><?php echo h($error) ?></li>
                <?php endforeach; ?>
            </ul>
            <a class="btn" href="test.php">Inapoi la test</a>
        </div>
    </body>
    </html>
    <?php
    exit; # scriptul se oșreste, nu are sens ssa continuam cu gradeTest()
}

$email = trim($_POST['email']);


if (emailExistsInResults($email)) { # daca exista deja emailul (testul a fost fct o data)
    ?>
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Test deja completat</title>
        <link rel="stylesheet" href="assets/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Ati completat deja testul</h1>
            <p>Adresa de email <strong><?php echo h($email) ?></strong> a rezolvat deja acest test anterior.</p>
            <a class="btn" href="index.php">Inapoi la pagina de start</a>
        </div>
    </body>
    </html>
    <?php
    exit;
}

$grading = gradeTest($_POST);
$saved = saveResult($email, $grading['total']);

if (!$saved) { # daca salvarea nu a reusit (emailul a fost adaugat intre validare si salvare)
    header('Location: index.php');
    exit;
}

// redirectionare catre pagina de rezultat, cu datele necesare transmise prin GET
header('Location: result.php?email=' . urlencode($email) . '&score=' . (int) $grading['total']);
exit;
