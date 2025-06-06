document.getElementById('form-ortofix').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio tradicional do formulário

    const selects = document.querySelectorAll('select[name="acento"]');
    const respostas = Array.from(selects).map(select => select.value);

    fetch('/corrigirortofix', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ respostas: respostas })
    })
    .then(res => res.json())
    .then(data => {
        const resultadoDiv = document.getElementById('resultado');
        resultadoDiv.innerHTML = '';

        data.resultado.forEach((item, index) => {
            const p = document.createElement('p');
            if (item.correto) {
                p.innerHTML = `✅ Palavra ${index + 1} correta!`;
                p.style.color = 'green';
            } else {
                p.innerHTML = `❌ Palavra ${index + 1} incorreta! Correto: <b>${item.resposta_correta}</b>`;
                p.style.color = 'red';
            }
            resultadoDiv.appendChild(p);
        });
    });
});

