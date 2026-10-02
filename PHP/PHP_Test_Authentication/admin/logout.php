<?php

require_once __DIR__ . '/includes/admin_functions.php';

startAdminSession();

$_SESSION = []; # goleste toate variabilele de sesiune

if (ini_get('session.use_cookies')) { # sterge si cookie-ul de sesiune, daca este folosit
    $params = session_get_cookie_params();
    setcookie(
        session_name(),
        '',
        time() - 42000,
        $params['path'],
        $params['domain'],
        $params['secure'],
        $params['httponly']
    );
}

session_destroy(); # distruge complet sesiunea pe server

header('Location: index.php');
exit;
