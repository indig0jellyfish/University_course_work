<?php
// Toate evenimentele (publice pentru utilizatorii logati) + rezervare de locuri
require __DIR__ . '/../includes/init.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $eventId = (int)($_POST['event_id'] ?? 0);
    $seatsRaw = trim($_POST['seats'] ?? '');
    $notes = trim($_POST['notes'] ?? '');

    if (!ctype_digit($seatsRaw) || (int)$seatsRaw < 1) {
        flash('error', 'Numărul de locuri trebuie să fie un număr întreg, minim 1.'); // init.php
    } elseif (mb_strlen($notes) > 500) {
        flash('error', 'Observațiile pot avea cel mult 500 de caractere.');
    } else {
        $seats = (int)$seatsRaw;

        // Rezervare sigura: tranzactie + blocarea randului evenimentului (FOR UPDATE),  Doua cereri simultane la acelasi eveniment sunt puse la coada => capacitatea nu poate fi depasita.
        $pdo = db();
        $pdo->beginTransaction();

        $stmt = $pdo->prepare('SELECT capacity FROM events WHERE id = ? FOR UPDATE');
        $stmt->execute([$eventId]);
        $capacity = $stmt->fetchColumn();

        if ($capacity === false) {
            flash('error', 'Evenimentul nu există.');
        } else {
            // locurile libere se calculeaza din BD la fiecare rezervare
            $stmt = $pdo->prepare('SELECT COALESCE(SUM(seats), 0) FROM reservations WHERE event_id = ?');
            $stmt->execute([$eventId]);
            $free = (int)$capacity - (int)$stmt->fetchColumn();

            if ($free <= 0) {
                flash('error', 'Înscrierea este blocată: nu mai sunt locuri disponibile.');
            } elseif ($seats > $free) {
                flash('error', "La acest eveniment au mai rămas $free locuri libere!");
            } else {
                $stmt = $pdo->prepare('INSERT INTO reservations (event_id, user_id, seats, notes) VALUES (?, ?, ?, ?)');
                $stmt->execute([$eventId, uid(), $seats, $notes === '' ? null : $notes]);
                flash('success', "Ai rezervat $seats loc(uri).");
            }
        }
        $pdo->commit();
    }
    redirect('pages/events.php');
}

$events = db()->query(
    'SELECT e.*, u.username AS owner_name, COALESCE(SUM(r.seats), 0) AS reserved
       FROM events e
       JOIN users u ON u.id = e.owner_id
       LEFT JOIN reservations r ON r.event_id = e.id
      GROUP BY e.id, u.username
      ORDER BY e.start_datetime ASC, e.id ASC'
)->fetchAll();

page_header('Toate evenimentele');
?>
<h1>Toate evenimentele</h1>
<?php if (!$events): ?>
    <div class="card muted">Nu există evenimente încă.</div>
<?php endif; ?>

<?php foreach ($events as $ev): $free = (int)$ev['capacity'] - (int)$ev['reserved']; ?>
<article class="card">
    <h2 style="margin-top:0"><?= e($ev['title']) ?></h2>
    <p class="muted">
        📅 <?= e(fmt_date($ev['start_datetime'])) ?> · 📍 <?= e($ev['location']) ?> ·
        👤 <?= e($ev['owner_name']) ?><?= (int)$ev['owner_id'] === uid() ? ' (tu)' : '' ?>
    </p>
    <p><?= nl2br(e($ev['description'])) ?></p>
    <p><strong>Locuri libere: <?= max(0, $free) ?></strong> din <?= (int)$ev['capacity'] ?></p>

    <?php if ($free <= 0): ?>
        <div class="alert error">Înscrierea este blocată: nu mai sunt locuri disponibile.</div>
    <?php else: ?>
    <form method="post">
        <input type="hidden" name="event_id" value="<?= (int)$ev['id'] ?>">
        <label>Număr de locuri <small class="muted">(1–<?= $free ?>)</small>
            <input type="number" name="seats" min="1" max="<?= $free ?>" value="1" required>
        </label>
        <label>Observații <small class="muted">(opțional, max. 500)</small>
            <textarea name="notes" rows="2" maxlength="500"></textarea>
        </label>
        <button class="btn">Rezervă</button>
    </form>
    <?php endif; ?>
</article>
<?php endforeach; ?>
<?php page_footer();
