<?php # test.php - formularul de test
require_once __DIR__ . '/includes/functions.php'; # inclue fisierul in program si executa continutul lui, o singura data
$questions = getQuestions();
?>

<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Completare test</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Completati testul</h1>

        <form action="submit_test.php" method="POST" novalidate>  
            <div class="form-group">
                <label for="email">Adresa de email:</label>
                <input type="email" id="email" name="email" required placeholder="nume@exemplu.com">
            </div>

            <?php foreach ($questions as $id => $q): ?>
                <div class="question">
                    <p class="question-title">
                        <?php echo h($q['label']) ?>. <?php echo h($q['question']) ?>
                        <?php if ($q['type'] === 'checkbox'): ?>
                            <em>(selectati toate variantele corecte)</em>
                        <?php endif; ?>
                    </p>

                    <?php if ($q['type'] === 'radio'): ?>
                        <?php foreach ($q['options'] as $key => $optionText): ?>
                            <label class="option">
                                <input type="radio" name="q<?php echo (int) $id ?>" value="<?php echo h($key)# au acelasi name pt ca aceste radio buttons fac parte din acelasi grup?>"> 
                                <?php echo h($optionText) ?>
                            </label><br>
                        <?php endforeach; ?>

                    <?php elseif ($q['type'] === 'checkbox'): ?>
                        <?php foreach ($q['options'] as $key => $optionText): ?>
                            <label class="option">
                                <input type="checkbox" name="q<?php echo (int) $id ?>[]" value="<?php echo h($key) ?>">
                                <?php echo h($optionText) ?>
                            </label><br>
                        <?php endforeach; ?>

                    <?php elseif ($q['type'] === 'text'): ?>
                        <input type="text" name="q<?php echo (int) $id ?>" placeholder="Raspunsul dvs.">
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>

            <button type="submit" class="btn">Trimite testul</button>
        </form>
    </div>
</body>
</html>
