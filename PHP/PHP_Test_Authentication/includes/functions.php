<?php
define('RESULTS_FILE', __DIR__ . '/../data/results.txt');

function getQuestions(): array # spune ca returneaza un arr
{
    return [
        1 => [
            'type' => 'radio',
            'label' => 'Q1',
            'question' => 'Care este numele real al lui Iron Man?',
            'options' => [
                'a' => 'Steve Rogers',
                'b' => 'Tony Stark',
                'c' => 'Bruce Banner',
                'd' => 'Peter Parker',
            ],
            'correct' => 'b',
        ],

        2 => [
            'type' => 'radio',
            'label' => 'Q2',
            'question' => 'Care dintre urmatorii este zeul tunetului in universul Marvel?',
            'options' => [
                'a' => 'Loki',
                'b' => 'Thor',
                'c' => 'Odin',
                'd' => 'Heimdall',
            ],
            'correct' => 'b',
        ],

        3 => [
            'type' => 'radio',
            'label' => 'Q3',
            'question' => 'Cum se numeste ciocanul lui Thor?',
            'options' => [
                'a' => 'Stormbreaker',
                'b' => 'Gungnir',
                'c' => 'Mjolnir',
                'd' => 'Hofund',
            ],
            'correct' => 'c',
        ],

        4 => [
            'type' => 'checkbox',
            'label' => 'Q4',
            'question' => 'Care dintre urmatorii sunt membri ai echipei Avengers? ',
            'options' => [
                'a' => 'Iron Man',
                'b' => 'Captain America',
                'c' => 'Thor',
                'd' => 'Darth Vader',
            ],
            'correct' => ['a', 'b', 'c'],
            'wrong' => ['d'],
        ],

        5 => [
            'type' => 'checkbox',
            'label' => 'Q5',
            'question' => 'Care dintre urmatorii sunt personaje din universul Marvel? ',
            'options' => [
                'a' => 'Spider-Man',
                'b' => 'Black Widow',
                'c' => 'Doctor Strange',
                'd' => 'Batman',
            ],
            'correct' => ['a', 'b', 'c'],
            'wrong' => ['d'],
        ],

        6 => [
            'type' => 'checkbox',
            'label' => 'Q6',
            'question' => 'Care dintre urmatoarele sunt Pietre ale Infinitului? (selectati toate variantele corecte)',
            'options' => [
                'a' => 'Piatra Timpului',
                'b' => 'Piatra Mintii',
                'c' => 'Piatra Realitatii',
                'd' => 'Piatra Puterii',
            ],
            'correct' => ['a', 'b', 'c', 'd'],
            'wrong' => [],
        ],

        7 => [
            'type' => 'text',
            'label' => 'Q7',
            'question' => 'Care este numele real al lui Spider-Man?',
            'correct' => 'peter parker',
        ],

        8 => [
            'type' => 'text',
            'label' => 'Q8',
            'question' => 'Cum se numeste planeta pe care locuieste Thor?',
            'correct' => 'asgard',
        ],

        9 => [
            'type' => 'text',
            'label' => 'Q9',
            'question' => 'Care este numele adevarat al lui Black Panther?',
            'correct' => 't challa',
        ],
    ];
}


function validateAnswers(array $post): array # primeste datele prin POST si return un arr cu errori
{
    $errors = [];

    # Validare email, e scris, e string, are format corect
    if (empty($post['email']) || !is_string($post['email'])) {
        $errors[] = 'Adresa de email este obligatorie.';
    } elseif (!filter_var($post['email'], FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Adresa de email introdusa nu este valida.';
    }

    $questions = getQuestions();

    foreach ($questions as $id => $q) {
        $fieldName = 'q' . $id;

        if ($q['type'] === 'checkbox') {
            if (isset($post[$fieldName]) && !is_array($post[$fieldName])) { # checkbox: e posib sa nu bifam nimic, insa de bifam, e acceptab macar 2 rasp (arr)
                $errors[] = "Raspunsul pentru intrebarea {$q['label']} este invalid (format neconform).";
            }
        } else {
            if (!isset($post[$fieldName]) || !is_string($post[$fieldName]) || trim($post[$fieldName]) === '') { # radio si text: exista, e string, nu e gol
                $errors[] = "Raspunsul pentru intrebarea {$q['label']} ({$q['question']}) este obligatoriu.";
            }
        }
    }

    return $errors;
}


function gradeTest(array $post): array
{
    $questions = getQuestions();
    $total = 0;
    $details = [];

    foreach ($questions as $id => $q) {
        $fieldName = 'q' . $id;
        $points = 0;

        if ($q['type'] === 'radio') {
            $selected = $post[$fieldName] ?? null;
            $points = ($selected === $q['correct']) ? 1 : 0;

        } elseif ($q['type'] === 'checkbox') {
            $selected = $post[$fieldName] ?? []; 
            if (!is_array($selected)) {
                $selected = []; # daca nu a bifat nim
            }
            # elimina duplicatele, rearanjeaza indicii arr, sorteaza rasp
            $selectedSet = array_values(array_unique($selected));
            sort($selectedSet);
            $correctSet = $q['correct'];
            sort($correctSet); # sort rasp corecte, apoi compara, daca e aceeasi, are toate punct, daca nu, are 0
            $points = ($selectedSet === $correctSet) ? 1 : 0;

        } elseif ($q['type'] === 'text') {
            $answer = $post[$fieldName] ?? ''; # ia rasp
            $normalizedAnswer = strtolower(trim($answer)); # normalizeara rasp norm si cele corecte
            $normalizedCorrect = strtolower(trim($q['correct']));
            $points = ($normalizedAnswer === $normalizedCorrect) ? 1 : 0; # compara
        }

        $details[$id] = $points;
        $total += $points;
    }

    return [
        'total' => $total,
        'max' => count($questions),
        'details' => $details,
    ];
}


function ensureResultsFile(): void # obtine folderul pt fisier, sua il creeaza
{
    $dir = dirname(RESULTS_FILE);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
    if (!file_exists(RESULTS_FILE)) {
        touch(RESULTS_FILE);
    }
}


function emailExistsInResults(string $email): bool  # verif daca emailul a mai dat testul
{
    ensureResultsFile();
    $email = strtolower(trim($email));

    $lines = file(RESULTS_FILE, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES); # citeste liniile din results.txt
    foreach ($lines as $line) {
        $parts = explode('|', $line);
        if (isset($parts[1]) && strtolower(trim($parts[1])) === $email) {
            return true;
        }
    }
    return false; # nu permite salvarea datelor again
}


function saveResult(string $email, int $score): bool
{
    ensureResultsFile();

    if (emailExistsInResults($email)) {
        return false; // deja a rezolvat testul
    }

    $line = date('Y-m-d H:i:s') . '|' . trim($email) . '|' . abs($score) . PHP_EOL; # scriem rez in fisier
    return (bool) file_put_contents(RESULTS_FILE, $line, FILE_APPEND | LOCK_EX); # adauga la sf fisierului, nu sterge rez vechi; block temp fisier in timp scrierii pt a reduce risc ca 2 scrieri simultane sas se amestece
}


function getAllResults(): array
{
    ensureResultsFile();
    $results = [];

    $lines = file(RESULTS_FILE, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        $parts = explode('|', $line);
        if (count($parts) === 3) { # transf formatul pt a fi mai usor de folosit
            $results[] = [
                'date' => $parts[0],
                'email' => $parts[1],
                'score' => (int) $parts[2],
            ];
        }
    }
    return $results;
}


function getAverageScore(): float
{
    $results = getAllResults();
    if (count($results) === 0) { # evitam imp la 0 daca nu ex rezultate
        return 0.0;
    }
    $sum = 0;
    foreach ($results as $r) {
        $sum += $r['score'];
    }
    return $sum / count($results);
}


function h(?string $value): string // transf caracterele html speciale in ceva sigur, impotriva xss
{
    return htmlspecialchars($value ?? '', ENT_QUOTES, 'UTF-8');
}
