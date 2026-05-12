(function() {
    const email = document.getElementById('id_email');
    const pwd1 = document.getElementById('id_password1');
    const pwd2 = document.getElementById('id_password2');
    const rules = document.querySelectorAll('.password-rules li');
    const matchHint = document.getElementById('passwordMatch');

    if (!pwd1 || !pwd2) return;  // якщо скрипт випадково підвантажився не на signup

    function check(rule, password, emailValue) {
        if (rule === 'length') return password.length >= 8;
        if (rule === 'notNumeric') return !/^\d+$/.test(password);
        if (rule === 'notSimilar') {
            if (!emailValue) return true;
            const local = emailValue.split('@')[0].toLowerCase();
            if (local.length < 3) return true;
            return !password.toLowerCase().includes(local);
        }
        return true;
    }

    function updateRules() {
        const password = pwd1.value;
        const emailValue = email ? email.value : '';
        const touched = password.length > 0;

        rules.forEach(li => {
            const icon = li.querySelector('.icon');
            if (!touched) {
                li.classList.remove('valid', 'invalid');
                icon.textContent = '○';
                return;
            }
            const ok = check(li.dataset.rule, password, emailValue);
            li.classList.toggle('valid', ok);
            li.classList.toggle('invalid', !ok);
            icon.textContent = ok ? '✓' : '✗';
        });

        updateMatch();
    }

    function updateMatch() {
        if (!matchHint) return;
        if (!pwd2.value) {
            matchHint.textContent = '';
            matchHint.className = 'small mt-1';
            return;
        }
        if (pwd1.value === pwd2.value) {
            matchHint.textContent = '✓ Паролі співпадають';
            matchHint.className = 'small mt-1 text-success';
        } else {
            matchHint.textContent = '✗ Паролі не співпадають';
            matchHint.className = 'small mt-1 text-danger';
        }
    }

    pwd1.addEventListener('input', updateRules);
    pwd2.addEventListener('input', updateMatch);
    if (email) email.addEventListener('input', updateRules);
})();