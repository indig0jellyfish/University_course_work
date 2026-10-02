<?php

require_once __DIR__ . '/../includes/functions.php'; 
require_once __DIR__ . '/includes/admin_functions.php';

startAdminSession();

// daca este deja autentificat trimite direct la dashboard, sesiunea activa a fost mai putin de 15 min
if (!empty($_SESSION['admin_logged_in']) && (time() - ($_SESSION['last_activity'] ?? 0)) <= SESSION_TIMEOUT_SECONDS) {
    header('Location: dashboard.php');
    exit;
}

$loginError = '';
$registerError = '';
$registerSuccess = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') { # daca formularul a fost de user transmis prin post
    $action = $_POST['action'] ?? '';

    if ($action === 'login') {
        $username = trim($_POST['username'] ?? '');
        $password = $_POST['password'] ?? '';

        if ($username === '' || $password === '') {
            $loginError = 'Introduceti numele de utilizator si parola.';
        } elseif (verifyLogin($username, $password)) {
            createAdminSession($username);
            header('Location: dashboard.php');
            exit;
        } else {
            $loginError = 'Nume de utilizator sau parola incorecta.';
        }
    } elseif ($action === 'register') {
        $username = trim($_POST['reg_username'] ?? '');
        $password = $_POST['reg_password'] ?? '';
        $passwordConfirm = $_POST['reg_password_confirm'] ?? '';

        if ($password !== $passwordConfirm) {
            $registerError = 'Parolele introduse nu coincid.';
        } else {
            $result = createAccount($username, $password);
            if ($result === '') {
                $registerSuccess = 'Cont creat cu succes! Va puteti autentifica acum.';
            } else {
                $registerError = $result;
            }
        }
    }
}

$timedOut = isset($_GET['timeout']);
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Admin - Autentificare</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Zona de administrare</h1>

        <?php if ($timedOut): ?>
            <p class="errors">Sesiunea a expirat din cauza inactivitatii (15 minute) sau a fost inchisa. Va rugam autentificati-va din nou.</p>
        <?php endif; ?>

        <h2>Autentificare</h2>
        <?php if ($loginError !== ''): ?>
            <p class="errors"><?= h($loginError) ?></p>
        <?php endif; ?>
        <form method="POST" novalidate>
            <input type="hidden" name="action" value="login">
            <div class="form-group">
                <label for="username">Utilizator:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Parola:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Autentificare</button>
        </form>

        <hr style="margin: 32px 0;">

        <h2>Nu aveti cont? Inregistrati-va</h2>
        <?php if ($registerError !== ''): ?>
            <p class="errors"><?= h($registerError) ?></p>
        <?php endif; ?>
        <?php if ($registerSuccess !== ''): ?>
            <p style="color:#1a7f37;font-weight:bold;"><?= h($registerSuccess) ?></p>
        <?php endif; ?>
        <form method="POST" novalidate>
            <input type="hidden" name="action" value="register">
            <div class="form-group">
                <label for="reg_username">Utilizator nou:</label>
                <input type="text" id="reg_username" name="reg_username" required>
            </div>
            <div class="form-group">
                <label for="reg_password">Parola (minim 8 caractere):</label>
                <input type="password" id="reg_password" name="reg_password" required minlength="8">
            </div>
            <div class="form-group">
                <label for="reg_password_confirm">Confirmare parola:</label>
                <input type="password" id="reg_password_confirm" name="reg_password_confirm" required minlength="8">
            </div>
            <button type="submit" class="btn">Creeaza cont</button>
        </form>
    </div>
</body>
</html>
