function gerarJSON() {
    // Obtenha os valores dos campos
    var nome = document.getElementById("firstname").value;
    var sobrenome = document.getElementById("lastname").value;
    var idade = document.getElementById("idade").value;
    var endereco = document.getElementById("endereco").value;
    var numero = document.getElementById("numero").value;
    var cep = document.getElementById("cep").value;
    var estado = document.getElementById("estado").value;
    var cidade = document.getElementById("cidade").value;
    var bairro = document.getElementById("bairro").value;

    // Verifique se todos os campos obrigatórios estão preenchidos
    if (nome && sobrenome && idade && endereco && numero && cep && estado && cidade && bairro) {
        // Obtenha os valores dos campos opcionais
        var complemento = document.getElementById("complemento").value;
        var febreCheckbox = document.querySelector('input[name="febre"]:checked');
        var febre = febreCheckbox ? febreCheckbox.value : "";
        var cabecaCheckbox = document.querySelector('input[name="cabeca"]:checked');
        var dor_de_cabeca = cabecaCheckbox ? cabecaCheckbox.value : "";
        var articulacoesCheckbox = document.querySelector('input[name="articulacoes"]:checked');
        var dor_nas_articulacoes = articulacoesCheckbox ? articulacoesCheckbox.value : "";
        var sangramentoCheckbox = document.querySelector('input[name="sangramento"]:checked');
        var sangramento = sangramentoCheckbox ? sangramentoCheckbox.value : "";

        // Crie o objeto de dados apenas com os campos preenchidos
        var dadosConsulta = {
            "nome": nome,
            "sobrenome": sobrenome,
            "idade": idade,
            "endereco": endereco,
            "numero": numero,
            "complemento": complemento,
            "cep": cep,
            "estado": estado,
            "cidade": cidade,
            "bairro": bairro,
            "febre": febre,
            "dor_de_cabeca": dor_de_cabeca,
            "dor_nas_articulacoes": dor_nas_articulacoes,
            "sangramento": sangramento
        };

        // Converter objeto JavaScript em JSON
        var jsonConsulta = JSON.stringify(dadosConsulta);
        console.log(jsonConsulta);

        // Enviar os dados para o servidor Flask via fetch()
        fetch('http://localhost:5000/receber_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonConsulta
        })
            .then(response => response.json())
            .then(data => {
                const formattedData = {
                    jsonData: JSON.stringify(data)
                };
                localStorage.setItem('consultaData', formattedData.jsonData);


            })
            .catch(error => {
                console.error('Erro ao enviar dados:', error);
                // Trate o erro conforme necessário
            });


        // Limpar os campos após o envio bem-sucedido
        document.getElementById("firstname").value = "";
        document.getElementById("lastname").value = "";
        document.getElementById("idade").value = "";
        document.getElementById("endereco").value = "";
        document.getElementById("numero").value = "";
        document.getElementById("complemento").value = "";
        document.getElementById("cep").value = "";
        document.getElementById("estado").value = "";
        document.getElementById("cidade").value = "";
        document.getElementById("bairro").value = "";

        // Desmarcar os botões de rádio selecionados, se houver
        if (febreCheckbox) {
            febreCheckbox.checked = false;
        }
        if (cabecaCheckbox) {
            cabecaCheckbox.checked = false;
        }
        if (articulacoesCheckbox) {
            articulacoesCheckbox.checked = false;
        }
        if (sangramentoCheckbox) {
            sangramentoCheckbox.checked = false;
        }

    } else {
        // Se algum campo obrigatório não estiver preenchido, exibir um alerta
        alert("Por favor, preencha todos os campos obrigatórios.");
    }
}

// Escute o evento de submissão do formulário
document.getElementById("consulta-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Evita o comportamento padrão de submissão do formulário

    // Chame a função gerarJSON para preparar e enviar os dados
    gerarJSON();
});
// Função para recuperar os dados do armazenamento local e exibir na tela
function mostrarDadosNaTela() {
    // Recuperar os dados do localStorage
    const consultaData = localStorage.getItem('consultaData');

    // Verificar se existem dados no localStorage
    if (consultaData) {
        const parsedData = JSON.parse(consultaData);
        console.log(parsedData); // Log dos dados recuperados

        // Verificar o valor de exame e adicionar mensagem correspondente
        let mensagem = '';
        if (parsedData.resultado_previsao.exame === 0) {
            mensagem = "Você pode consultar um profissional de plantão para te orientar e examinar.";
        } else if (parsedData.resultado_previsao.exame === 1) {
            mensagem = "Você precisa ir ao hospital mais próximo.";
        }

        // Formatar os dados em HTML
        const htmlContent = `
            <p>Nome: ${parsedData.resultado_previsao.nome}</p>
            <p>Exame: ${parsedData.resultado_previsao.exame}</p>
            <p>${mensagem}</p>
        `;

        // Inserir o HTML na div com id "resultado"
        document.getElementById('resultado').innerHTML = htmlContent;

        // Tornar a div visível
        document.getElementById('resultado').style.display = 'block';
    } else {
        console.log('Nenhum dado de consulta encontrado no armazenamento local.');
    }
}

// Chamar a função para mostrar os dados na tela quando a página for carregada
document.addEventListener('DOMContentLoaded', mostrarDadosNaTela);
