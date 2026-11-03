<?php
require __DIR__ . '/../includes/init.php';
require_login();

$id = (int)($_GET['id'] ?? 0);
$event = null;

if ($id) {
    // doar proprietarul poate edita: WHERE id = ? AND owner_id = ?
    $stmt = db()->prepare('SELECT * FROM events WHERE id = ? AND owner_id = ?');
    $stmt->execute([$id, uid()]);
    $event = $stmt->fetch();
    if (!$event) {
        flash('error', 'Evenimentul nu există sau nu ai dreptul să îl editezi.');
        redirect('pages/dashboard.php');
    }
}

$v = $event
    ? [
        'title' => $event['title'], 'description' => $event['description'], 'location' => $event['location'],
        'start_datetime' => date('Y-m-d\TH:i', strtotime($event['start_datetime'])), 'capacity' => (string)$event['capacity'],
    ] // editam
    : ['title' => '', 'description' => '', 'location' => '', 'start_datetime' => '', 'capacity' => '']; // cream
$err = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    [$v, $err] = validate_event($_POST);

    if (!$err) {
        $start = str_replace('T', ' ', $v['start_datetime']) . ':00';
        if ($event) { // UPDATE
            $stmt = db()->prepare(
                'UPDATE events SET title = ?, description = ?, location = ?, start_datetime = ?, capacity = ?
                  WHERE id = ? AND owner_id = ?'
            );
            $stmt->execute([$v['title'], $v['description'], $v['location'], $start, (int)$v['capacity'], $id, uid()]);
            flash('success', 'Evenimentul a fost actualizat.');
        } else { // INSERT
            $stmt = db()->prepare(
                'INSERT INTO events (owner_id, title, description, location, start_datetime, capacity) VALUES (?, ?, ?, ?, ?, ?)'
            );
            $stmt->execute([uid(), $v['title'], $v['description'], $v['location'], $start, (int)$v['capacity']]);
            flash('success', 'Evenimentul a fost creat.');
        }
        redirect('pages/dashboard.php');
    }
}

page_header($event ? 'Editare eveniment' : 'Eveniment nou');
?>
<h1><?= $event ? 'Editare eveniment' : 'Eveniment nou' ?></h1>
<form method="post" class="card" novalidate>
    <label for="title">Titlu <small class="muted">(3–120 caractere)</small></label>
    <input type="text" id="title" name="title" maxlength="120" value="<?= e($v['title']) ?>">
    <?= field_error($err, 'title') ?>

    <label for="description">Descriere</label>
    <textarea id="description" name="description" rows="5" maxlength="2000"><?= e($v['description']) ?></textarea>
    <?= field_error($err, 'description') ?>

    <label for="location">Locație</label>
    <input type="text" id="location" name="location" maxlength="150" value="<?= e($v['location']) ?>">
    <?= field_error($err, 'location') ?>

    <label for="start_datetime">Data și ora</label>
    <input type="datetime-local" id="start_datetime" name="start_datetime" value="<?= e($v['start_datetime']) ?>">
    <?= field_error($err, 'start_datetime') ?>

    <label for="capacity">Număr maxim de locuri <small class="muted">(1–500)</small></label>
    <input type="number" id="capacity" name="capacity" min="1" max="500" value="<?= e($v['capacity']) ?>">
    <?= field_error($err, 'capacity') ?>

    <button class="btn"><?= $event ? 'Salvează modificările' : 'Creează evenimentul' ?></button>
    <a class="btn outline" href="<?= e(url('pages/dashboard.php')) ?>">Anulează</a>
</form>
<?php page_footer();
