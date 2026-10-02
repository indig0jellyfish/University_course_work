<?php

define('ACCOUNTS_FILE', __DIR__ . '/../../data/accounts.txt'); # stocarea conturilor, parola sub hash
define('SESSION_TIMEOUT_SECONDS', 15 * 60); // 15 minute


function ensureAccountsFile(): void # asigura ca fisierul de conturi si folderul data/ exista
{
    $dir = dirname(ACCOUNTS_FILE);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
    if (!file_exists(ACCOUNTS_FILE)) {
        touch(ACCOUNTS_FILE);
    }
}


function getAllAccounts(): array # citeste conturi fisier format linie username|passwordHash
{
    ensureAccountsFile();
    $accounts = [];

    $lines = file(ACCOUNTS_FILE, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        $parts = explode('|', $line, 2);
        if (count($parts) === 2) {
            $accounts[$parts[0]] = $parts[1]; // username => hash
        }
    }
    return $accounts;
}


function accountExists(string $username): bool # verfi daca exista
{
    $accounts = getAllAccounts();
    return array_key_exists($username, $accounts);
}


function createAccount(string $username, string $password): string # creeaza cont admin
{
    $username = trim($username);

    if ($username === '') {
        return 'Numele de utilizator este obligatoriu.';
    }
    if (strlen($password) < 8) {
        return 'Parola trebuie sa aiba cel putin 8 caractere.';
    }
    if (accountExists($username)) {
        return 'Acest nume de utilizator este deja folosit.';
    }

    ensureAccountsFile();
    $hash = password_hash($password, PASSWORD_DEFAULT);
    $line = $username . '|' . $hash . PHP_EOL;
    file_put_contents(ACCOUNTS_FILE, $line, FILE_APPEND | LOCK_EX); # salvam in file

    return '';
}


function verifyLogin(string $username, string $password): bool # verif datele de logare fata de cont stocat
{
    $accounts = getAllAccounts();
    if (!array_key_exists($username, $accounts)) {
        return false;
    }
    return password_verify($password, $accounts[$username]);
}


function startAdminSession(): void # porneste sesiunea php daca nu este activa
{
    if (session_status() !== PHP_SESSION_ACTIVE) {
        session_start();
    }
}


function createAdminSession(string $username): void # creeaza sesiunea de administrator dupa autentificare cu succes
{
    startAdminSession();
    session_regenerate_id(true);
    $_SESSION['admin_logged_in'] = true;
    $_SESSION['admin_username'] = $username;
    $_SESSION['last_activity'] = time();
}


function requireAdminSession(): void # verif existenta unei ses admin valide si neexpir
{
    startAdminSession();

    $loggedIn = $_SESSION['admin_logged_in'] ?? false;
    $lastActivity = $_SESSION['last_activity'] ?? null;

    $expired = $lastActivity !== null && (time() - $lastActivity) > SESSION_TIMEOUT_SECONDS;

    if (!$loggedIn || $expired) {
        $_SESSION = [];
        session_destroy();
        header('Location: index.php?timeout=1');
        exit;
    }

    $_SESSION['last_activity'] = time(); # actualizeaza timpul ultimei activitati
}
