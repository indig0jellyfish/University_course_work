<?php
// Incarcat in fiecare pagina: setari, sesiune, BD, validari si layout (header/footer)

const BASE_URL = '/event-booking';
date_default_timezone_set('Europe/Chisinau');
ini_set('display_errors', '0'); // erorile se scriu in log, nu se arata utilizatorului
ini_set('log_errors', '1');

//  SESIUNE 
ini_set('session.use_strict_mode', '1');
session_set_cookie_params(['httponly' => true]);
session_start();

//  BAZA DE DATE (PDO) 
function db(): PDO
{
    static $pdo = null;
    return $pdo ??= new PDO(
        'mysql:host=127.0.0.1;port=3306;dbname=event_booking;charset=utf8mb4',
        'root',
        '',
        [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false, // prepared statements reale
        ]
    );
}

//  FUNCTII AJUTATOARE 
function e($v): string { return htmlspecialchars((string)$v, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); } // protectie XSS

function url(string $path): string { return BASE_URL . '/' . $path; }

function redirect(string $path): never { header('Location: ' . url($path)); exit; }

function flash(string $type, string $msg): void { $_SESSION['flash'][] = [$type, $msg]; } // mesaj afisat o singura data, dupa redirect

function fmt_date(string $dt): string { return date('d.m.Y H:i', strtotime($dt)); }

function uid(): int { return (int)($_SESSION['user_id'] ?? 0); }

// Pagina protejata: fara sesiune => redirectare la formularul de login (cerinta 9.c)
function require_login(): void { if (!uid()) redirect('index.php'); }

function field_error(array $errors, string $key): string { return isset($errors[$key]) ? '<div class="field-error">' . e($errors[$key]) . '</div>' : ''; }


//  VALIDARE SERVER-SIDE 
// Evenimentul: returneaza [valori curatate, erori]
function validate_event(array $in): array
{
    $v = [];
    foreach (['title', 'description', 'location', 'start_datetime', 'capacity'] as $k) {
        $v[$k] = trim((string)($in[$k] ?? ''));
    }
    $err = [];

    // Titlu: 3-120 caractere (mb_strlen numara litere cu diacritice ca 1 caracter; trim elimina spatiile de la capete)
    $len = mb_strlen($v['title']);
    if ($len < 3 || $len > 120) {
        $err['title'] = "Titlul trebuie să aibă între 3 și 120 de caractere (acum: $len).";
    }
    if ($v['description'] === '' || mb_strlen($v['description']) > 2000) {
        $err['description'] = 'Descrierea este obligatorie (max. 2000 de caractere).';
    }
    if ($v['location'] === '' || mb_strlen($v['location']) > 150) {
        $err['location'] = 'Locația este obligatorie (max. 150 de caractere).';
    }

    // Data: format exact + data reala din calendar (30 februarie => invalid) + nu din trecut
    $d = DateTimeImmutable::createFromFormat('!Y-m-d\TH:i', $v['start_datetime']);
    if (!$d || $d->format('Y-m-d\TH:i') !== $v['start_datetime']) {
        $err['start_datetime'] = 'Data și ora nu sunt valide.';
    } elseif ($d <= new DateTimeImmutable()) {
        $err['start_datetime'] = 'Data și ora trebuie să fie în viitor.';
    }

    // Capacitate: numar intreg 1..500
    if (!ctype_digit($v['capacity']) || (int)$v['capacity'] < 1 || (int)$v['capacity'] > 500) {
        $err['capacity'] = 'Numărul de locuri trebuie să fie un număr întreg între 1 și 500.';
    }
    return [$v, $err];
}

//  LAYOUT 
function page_header(string $title): void
{
    ?><!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($title) ?> · Rezervări evenimente</title>
    <link rel="stylesheet" href="<?= e(url('css/style.css')) ?>">
</head>
<body>
<header class="topbar">
    <div class="container">
        <strong>🎟️ Rezervări evenimente</strong>
        <?php if (uid()): ?>
        <nav>
            <a href="<?= e(url('pages/dashboard.php')) ?>">Panoul meu</a>
            <a href="<?= e(url('pages/events.php')) ?>">Toate evenimentele</a>
            <a href="<?= e(url('pages/event.php')) ?>">+ Eveniment nou</a>
            <span>👤 <?= e($_SESSION['username']) ?></span>
            <form method="post" action="<?= e(url('index.php')) ?>" class="inline">
                <input type="hidden" name="action" value="logout">
                <button class="btn small outline">Ieșire</button>
            </form>
        </nav>
        <?php endif; ?>
    </div>
</header>
<main class="container">
<?php
    foreach ($_SESSION['flash'] ?? [] as [$type, $msg]) {
        echo '<div class="alert ' . e($type) . '">' . e($msg) . '</div>';
    }
    unset($_SESSION['flash']);
}

function page_footer(): void
{
    echo "</main>\n</body>\n</html>";
}
