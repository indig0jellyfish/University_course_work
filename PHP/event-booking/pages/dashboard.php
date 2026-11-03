<?php
// Panoul utilizatorului: evenimentele mele (READ + DELETE) si rezervarile mele (READ + anulare).
require __DIR__ . '/../includes/init.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = (int)($_POST['id'] ?? 0);

    if (($_POST['action'] ?? '') === 'delete_event') {
        // doar proprietarul; rezervarile se sterg prin ON DELETE CASCADE
        $stmt = db()->prepare('DELETE FROM events WHERE id = ? AND owner_id = ?');
        $stmt->execute([$id, uid()]);
        $stmt->rowCount() ? flash('success', 'Evenimentul a fost șters.')
                          : flash('error', 'Evenimentul nu există sau nu ai dreptul să îl ștergi.');
    }

    if (($_POST['action'] ?? '') === 'cancel_reservation') {
        // doar rezervarea proprie; locurile devin libere (disponibilul se calculeaza din SUM(seats))
        $stmt = db()->prepare('DELETE FROM reservations WHERE id = ? AND user_id = ?');
        $stmt->execute([$id, uid()]);
        $stmt->rowCount() ? flash('success', 'Rezervarea a fost anulată. Locurile sunt din nou disponibile.')
                          : flash('error', 'Rezervarea nu există sau nu îți aparține.');
    }
    redirect('pages/dashboard.php');
}

// Evenimentele proprii: ultimul adaugat = primul in lista
$stmt = db()->prepare(
    'SELECT e.*, COALESCE(SUM(r.seats), 0) AS reserved
       FROM events e LEFT JOIN reservations r ON r.event_id = e.id
      WHERE e.owner_id = ?
      GROUP BY e.id
      ORDER BY e.created_at DESC, e.id DESC'
);
$stmt->execute([uid()]);
$events = $stmt->fetchAll();

$stmt = db()->prepare(
    'SELECT r.id, r.seats, r.notes, e.title, e.location, e.start_datetime
       FROM reservations r JOIN events e ON e.id = r.event_id
      WHERE r.user_id = ?
      ORDER BY r.created_at DESC, r.id DESC'
);
$stmt->execute([uid()]);
$reservations = $stmt->fetchAll();

page_header('Panoul meu');
?>
<h1>Evenimentele mele</h1>
<?php if (!$events): ?>
    <div class="card muted">Nu ai creat încă niciun eveniment.</div>
<?php else: ?>
<div class="card table-wrap">
    <table>
        <tr><th>Titlu</th><th>Data și ora</th><th>Locație</th><th>Rezervate / Total</th><th></th></tr>
        <?php foreach ($events as $ev): ?>
        <tr>
            <td><?= e($ev['title']) ?></td>
            <td><?= e(fmt_date($ev['start_datetime'])) ?></td>
            <td><?= e($ev['location']) ?></td>
            <td><?= (int)$ev['reserved'] ?> / <?= (int)$ev['capacity'] ?></td>
            <td>
                <a class="btn small outline" href="<?= e(url('pages/event.php?id=' . $ev['id'])) ?>">Editează</a>
                <form method="post" class="inline" onsubmit="return confirm('Ștergi evenimentul și rezervările lui?');">
                    <input type="hidden" name="action" value="delete_event">
                    <input type="hidden" name="id" value="<?= (int)$ev['id'] ?>">
                    <button class="btn small danger">Șterge</button>
                </form>
            </td>
        </tr>
        <?php endforeach; ?>
    </table>
</div>
<?php endif; ?>

<h2>Rezervările mele</h2>
<?php if (!$reservations): ?>
    <div class="card muted">Nu ai nicio rezervare. Vezi <a href="<?= e(url('pages/events.php')) ?>">toate evenimentele</a>.</div>
<?php else: ?>
<div class="card table-wrap">
    <table>
        <tr><th>Eveniment</th><th>Data și ora</th><th>Locație</th><th>Locuri</th><th>Observații</th><th></th></tr>
        <?php foreach ($reservations as $r): ?>
        <tr>
            <td><?= e($r['title']) ?></td>
            <td><?= e(fmt_date($r['start_datetime'])) ?></td>
            <td><?= e($r['location']) ?></td>
            <td><?= (int)$r['seats'] ?></td>
            <td><?= e($r['notes']) ?></td>
            <td>
                <form method="post" class="inline" onsubmit="return confirm('Anulezi rezervarea?');">
                    <input type="hidden" name="action" value="cancel_reservation">
                    <input type="hidden" name="id" value="<?= (int)$r['id'] ?>">
                    <button class="btn small danger">Anulează</button>
                </form>
            </td>
        </tr>
        <?php endforeach; ?>
    </table>
</div>
<?php endif; ?>
<?php page_footer();
