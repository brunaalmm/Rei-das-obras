// dashboard.js

function atualizarHorario() {
  const agora = new Date();

  // Hora
  const horas = agora.getHours().toString().padStart(2, '0');
  const minutos = agora.getMinutes().toString().padStart(2, '0');
  const segundos = agora.getSeconds().toString().padStart(2, '0');
  document.getElementById('hora').textContent = `${horas}:${minutos}:${segundos}`;

  // Dia da semana
  const diasSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
  const diaSemana = diasSemana[agora.getDay()];
  document.getElementById('dia-semana').textContent = diaSemana;

  // Dia e mês
  const dia = agora.getDate().toString().padStart(2, '0');
  const meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
  const mes = meses[agora.getMonth()];
  document.getElementById('data').textContent = `${dia} de ${mes}`;
}

setInterval(atualizarHorario, 1000);
atualizarHorario();

// Gráfico de Faturamento
function renderizarGraficoFaturamento() {
  const ctxFat = document.getElementById('faturamentoChart');
  new Chart(ctxFat, {
    type: 'line',
    data: {
      labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
      datasets: [{
        label: 'Faturamento (R$)',
        data: [12000, 19000, 3000, 5000, 22000, 15000],
        borderColor: '#045cd0',
        borderWidth: 2,
        fill: false,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' }
      }
    }
  });
}

// Gráfico de Vendas por Categoria
function renderizarGraficoCategorias(categorias, totais) {
  const ctxCat = document.getElementById('categoriaChart');
  new Chart(ctxCat, {
    type: 'pie',
    data: {
      labels: categorias,
      datasets: [{
        label: 'Vendas por Categoria',
        data: totais,
        backgroundColor: ['#045cd0', '#67a3ff', '#1e90ff', '#ff6200', '#ff8c42', '#ffaa75']
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });
}