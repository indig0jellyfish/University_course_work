<?php
// Pagina de start (publica): autentificare + SignUp + logout.
require __DIR__ . '/includes/init.php';

$action = $_SERVER['REQUEST_METHOD'] === 'POST' ? ($_POST['action'] ?? '') : '';

//  LOGOUT 
if ($action === 'logout') {
    $_SESSION = [];
    session_destroy();
    session_start();
    flash('success', 'Te-ai deconectat cu succes.');
    redirect('index.php');
}

if (uid()) { // init.php
    redirect('pages/dashboard.php');
}

$loginError = '';
$err = [];
$v = ['username' => '', 'email' => ''];

//  LOGIN 
if ($action === 'login') {
    $stmt = db()->prepare('SELECT id, username, password_hash FROM users WHERE username = ?');
    $stmt->execute([trim($_POST['username'] ?? '')]);
    $user = $stmt->fetch();

    if ($user && password_verify($_POST['password'] ?? '', $user['password_hash'])) {
        session_regenerate_id(true); // previne session fixation 9.b
        $_SESSION['user_id']  = (int)$user['id'];
        $_SESSION['username'] = $user['username'];
        redirect('pages/dashboard.php');
    }
    $loginError = 'Nume de utilizator sau parolă incorecte.'; // acelasi mesaj pentru ambele cazuri
}

//  SIGNUP 
if ($action === 'signup') {
    $v['username'] = trim($_POST['username'] ?? '');
    $v['email'] = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';

    if (!preg_match('/^[A-Za-z0-9_]{3,30}$/', $v['username'])) {
        $err['username'] = 'Numele de utilizator: 3–30 caractere (litere latine, cifre, „_”).';
    }
    if (strlen($v['email']) > 190 || !filter_var($v['email'], FILTER_VALIDATE_EMAIL)) {
        $err['email'] = 'Adresa de email nu este validă.';
    }
    if (strlen($password) < 8 || !preg_match('/[A-Za-z]/', $password) || !preg_match('/\d/', $password)) {
        $err['password'] = 'Parola: minim 8 caractere, cu cel puțin o literă și o cifră.';
    }

    if (!$err) { // daca nu exista erori, continuam inregistr
        try {
            // password_hash() = bcrypt cu salt aleator; parola in clar nu se salveaza niciodata
            $stmt = db()->prepare('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)');
            $stmt->execute([$v['username'], $v['email'], password_hash($password, PASSWORD_DEFAULT)]);
            flash('success', 'Contul a fost creat. Te poți autentifica acum.');
            redirect('index.php');
        } catch (PDOException $ex) {
            if ($ex->getCode() !== '23000') { // 23000 = incalcare UNIQUE (username/email deja folosit)
                throw $ex;
            }
            $err['username'] = 'Numele de utilizator sau email-ul este deja folosit.';
        }
    }
}

page_header('Autentificare');
?>
<div class="cols">
    <section class="card">
        <h1>Autentificare</h1>
        <?php if ($loginError): ?><div class="alert error"><?= e($loginError) ?></div><?php endif; ?>
        <form method="post">
            <input type="hidden" name="action" value="login">
            <label for="l_username">Nume de utilizator</label>
            <input type="text" id="l_username" name="username" required maxlength="30">
            <label for="l_password">Parolă</label>
            <input type="password" id="l_password" name="password" required>
            <button class="btn">Intră în cont</button>
        </form>
    </section>

    <section class="card">
        <h1>SignUp – cont nou</h1>
        <form method="post" novalidate>
            <input type="hidden" name="action" value="signup">
            <label for="s_username">Nume de utilizator</label>
            <input type="text" id="s_username" name="username" maxlength="30" value="<?= e($v['username']) ?>">
            <?= field_error($err, 'username') ?>
            <label for="s_email">Email</label>
            <input type="email" id="s_email" name="email" maxlength="190" value="<?= e($v['email']) ?>">
            <?= field_error($err, 'email') ?>
            <label for="s_password">Parolă <small class="muted">(min. 8, literă + cifră)</small></label>
            <input type="password" id="s_password" name="password">
            <?= field_error($err, 'password') ?>
            <button class="btn">Creează cont</button>
        </form>
    </section>
</div>
<?php page_footer();
