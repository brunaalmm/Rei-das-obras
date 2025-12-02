// Exibe o modal para adicionar produto
document.getElementById("btn-add-produto").addEventListener("click", function() {
    const modal = new bootstrap.Modal(document.getElementById("produtoModal"));
    modal.show();
    
    // Configura o filtro após o modal ser mostrado
    setupProdutoFilter();
});

// Configura o filtro de produtos
function setupProdutoFilter() {
    const filterInput = document.getElementById("produto-filter");
    const produtoList = document.getElementById("produto-list");
    
    if (filterInput && produtoList) {
        filterInput.addEventListener("input", function() {
            const termo = this.value.toLowerCase();
            const linhas = produtoList.querySelectorAll("tr");
            
            linhas.forEach(linha => {
                const textoLinha = linha.textContent.toLowerCase();
                linha.style.display = textoLinha.includes(termo) ? "" : "none";
            });
        });
        
        // Dispara o evento input para filtrar imediatamente se houver valor
        if (filterInput.value) {
            filterInput.dispatchEvent(new Event('input'));
        }
    }
}

// Adiciona produto à tabela
function setupSelecionarButtons() {
    document.querySelectorAll(".btn-selecionar").forEach(btn => {
        btn.addEventListener("click", function() {
            const id = this.getAttribute("data-id");
            const nome = this.getAttribute("data-nome");
            const preco = parseFloat(this.getAttribute("data-preco"));
            const tbody = document.getElementById("produtos-body");

            // Verifica se o produto já foi adicionado
            const produtoExistente = Array.from(tbody.querySelectorAll('input[name="produto_id[]"]'))
                .some(input => input.value === id);
            
            if (produtoExistente) {
                alert("Este produto já foi adicionado ao pedido!");
                return;
            }

            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>
                    <input type="hidden" name="produto_id[]" value="${id}">
                    ${nome}
                </td>
                <td><input type="number" name="quantidade[]" value="1" min="1" class="form-control quantidade-input" oninput="atualizaSubtotal(this)"></td>
                <td>R$ <span class="preco">${preco.toFixed(2)}</span></td>
                <td>R$ <span class="subtotal">${preco.toFixed(2)}</span></td>
                <td>
                    <button type="button" class="btn btn-danger btn-sm" onclick="removerLinha(this)">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
            bootstrap.Modal.getInstance(document.getElementById("produtoModal")).hide();
        });
    });
}

// Remove uma linha
function removerLinha(button) {
    if (confirm("Tem certeza que deseja remover este produto?")) {
        button.closest("tr").remove();
        atualizaTotalGeral();
    }
}

// Atualiza subtotal
function atualizaSubtotal(input) {
    const tr = input.closest("tr");
    const qtd = parseInt(input.value) || 0;
    const preco = parseFloat(tr.querySelector(".preco").textContent) || 0;
    const subtotal = qtd * preco;

    tr.querySelector(".subtotal").textContent = subtotal.toFixed(2);
    atualizaTotalGeral();
}

// Atualiza total geral
function atualizaTotalGeral() {
    const subtotais = document.querySelectorAll("#produtos-body .subtotal");
    let total = 0;
    
    subtotais.forEach(span => {
        total += parseFloat(span.textContent) || 0;
    });

    document.getElementById("total-geral").textContent = total.toFixed(2);
}

// Inicializa tudo quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Configura os botões de seleção
    setupSelecionarButtons();
    
    // Atualiza totais para produtos existentes
    document.querySelectorAll(".quantidade-input").forEach(input => {
        atualizaSubtotal(input);
    });
    
    // Configura o filtro para o caso de o modal já estar aberto
    setupProdutoFilter();
});