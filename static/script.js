function adicionarLinha() {
    const container = document.getElementById('container-itens');
    const primeiraLinha = document.querySelector('.item-linha');
    const novaLinha = primeiraLinha.cloneNode(true);

    // Limpa valores da nova linha
    novaLinha.querySelector('.select-produto').value = "";
    novaLinha.querySelector('.input-qtd').value = 1;

    container.appendChild(novaLinha);
}

function removerLinha(botao) {
    const linhas = document.querySelectorAll('.item-linha');

    // Impede remover a última linha
    if (linhas.length === 1) {
        alert("O pedido precisa ter pelo menos um item.");
        return;
    }

    botao.closest('.item-linha').remove();
}

// Monta o JSON no submit
document.getElementById('formPedido').addEventListener('submit', function (e) {
    const linhas = document.querySelectorAll('.item-linha');
    let itens = [];

    linhas.forEach(linha => {
        const select = linha.querySelector('.select-produto');
        const qtd = parseInt(linha.querySelector('.input-qtd').value);

        if (select.value && qtd > 0) {
            const option = select.options[select.selectedIndex];

            itens.push({
                id: select.value,
                name: option.dataset.name,
                price: parseInt(option.dataset.price),
                quantity: qtd
            });
        }
    });

    if (itens.length === 0) {
        e.preventDefault();
        alert("Adicione pelo menos um item ao pedido.");
        return;
    }

    document.getElementById('itensJson').value = JSON.stringify(itens);
});