<?php

require_once __DIR__ . '/../includes/functions.php';
require_once __DIR__ . '/includes/admin_functions.php';

requireAdminSession(); // redirect automat catre index.php daca sesiunea nu e valida / a expirat

$username = h($_SESSION['admin_username'] ?? '');
$results = getAllResults(); # din functions php

$scores = array_map(fn($r) => $r['score'], $results); # ia doar punctajele
$count = count($scores);
$average = $count > 0 ? array_sum($scores) / $count : 0;
$min = $count > 0 ? min($scores) : 0;
$max = $count > 0 ? max($scores) : 0;

$timeoutMs = SESSION_TIMEOUT_SECONDS * 1000; # timeout-ul de sesiune ramas, transmis catre JS pentru auto-logout la inactivitate
?>

<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Admin - Dashboard</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <div class="container">
        <div class="logout-bar">
            <h1 style="margin:0;">Panou de analiza</h1>
            <form method="POST" action="logout.php" style="margin:0;">
                <button type="submit" class="btn">Deconectare</button>
            </form>
        </div>
        <p>Autentificat ca: <strong><?= $username ?></strong></p>

        <div class="stats">
            <div class="stat-card">
                <span class="value"><?= (int) $count ?></span>
                Numar utilizatori
            </div>
            <div class="stat-card">
                <span class="value"><?= number_format($average, 2) ?></span>
                Media punctajelor
            </div>
            <div class="stat-card">
                <span class="value"><?= (int) $min ?></span>
                Punctaj minim
            </div>
            <div class="stat-card">
                <span class="value"><?= (int) $max ?></span>
                Punctaj maxim
            </div>
        </div>

        <h2>Toate rezultatele</h2>
        <?php if ($count === 0): ?>
            <p>Nu exista inca rezultate inregistrate.</p>
        <?php else: ?>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Data / ora</th>
                        <th>Email</th>
                        <th>Punctaj</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($results as $i => $r): ?>
                        <tr>
                            <td><?= (int) ($i + 1) ?></td>
                            <td><?= h($r['date']) ?></td>
                            <td><?= h($r['email']) ?></td>
                            <td><?= (int) $r['score'] ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php endif; ?>
    </div>

    <script>
        // auto-logout la inactivitate (15 min), sincronizat cu verif server-side
        const TIMEOUT_MS = <?= (int) $timeoutMs ?>;
        let inactivityTimer;

        function resetInactivityTimer() {
            clearTimeout(inactivityTimer);
            inactivityTimer = setTimeout(() => {
                window.location.href = 'logout.php';
            }, TIMEOUT_MS);
        }

        ['mousemove', 'keydown', 'click', 'scroll'].forEach(evt =>
            document.addEventListener(evt, resetInactivityTimer)
        );
        resetInactivityTimer();
    </script>
</body>
</html>
