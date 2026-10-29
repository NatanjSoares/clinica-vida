/* ==========================================================
   Clínica Vida+ — JavaScript do navegador

   Atenção: a validação DE VERDADE continua no Python
   (validacoes.py). Aqui é só um reforço para o usuário ver
   o erro antes de enviar e para facilitar a digitação.

   Cada função só age se encontrar os elementos na página,
   então o mesmo arquivo serve para todas as telas.
   ========================================================== */

(function () {
    "use strict";

    /* ---------- funções de texto ---------- */

    function somenteDigitos(valor) {
        return valor.replace(/\D/g, "");
    }

    // "11999999999" -> "(11) 99999-9999"   |   "1133334444" -> "(11) 3333-4444"
    function formatarTelefone(valor) {
        var d = somenteDigitos(valor).slice(0, 11);
        if (d.length === 0) { return ""; }
        if (d.length <= 2) { return "(" + d; }

        var ddd = d.slice(0, 2);
        var resto = d.slice(2);
        var tamanhoPrimeiraParte = d.length > 10 ? 5 : 4;  // celular tem 9 dígitos
        var parte1 = resto.slice(0, tamanhoPrimeiraParte);
        var parte2 = resto.slice(tamanhoPrimeiraParte);

        return "(" + ddd + ") " + parte1 + (parte2 ? "-" + parte2 : "");
    }

    // "11111111111" -> "111.111.111-11"
    function formatarCpf(valor) {
        var d = somenteDigitos(valor).slice(0, 11);
        var resultado = d.slice(0, 3);
        if (d.length > 3) { resultado += "." + d.slice(3, 6); }
        if (d.length > 6) { resultado += "." + d.slice(6, 9); }
        if (d.length > 9) { resultado += "-" + d.slice(9, 11); }
        return resultado;
    }

    // minúsculas e sem acento, para comparar "João" com "joao"
    function normalizar(texto) {
        return texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    /* ---------- máscaras nos campos ---------- */

    function aplicarMascara(campo, formatador) {
        if (!campo) { return; }
        campo.value = formatador(campo.value);
        campo.addEventListener("input", function () {
            campo.value = formatador(campo.value);
        });
    }

    function aceitarSoDigitos(campo) {
        if (!campo) { return; }
        campo.addEventListener("input", function () {
            campo.value = somenteDigitos(campo.value);
        });
    }

    /* ---------- validação visual do formulário de cadastro ---------- */

    function limparErro(campo) {
        campo.classList.remove("campo-invalido");
        var aviso = campo.parentNode.querySelector(".mensagem-campo");
        if (aviso) { aviso.remove(); }
    }

    function mostrarErro(campo, mensagem) {
        limparErro(campo);
        campo.classList.add("campo-invalido");
        var aviso = document.createElement("small");
        aviso.className = "mensagem-campo";
        aviso.textContent = mensagem;
        campo.parentNode.appendChild(aviso);
    }

    function validarNome(campo) {
        if (campo.value.trim() === "") {
            mostrarErro(campo, "O nome não pode estar vazio.");
            return false;
        }
        limparErro(campo);
        return true;
    }

    function validarIdade(campo) {
        if (campo.value.trim() === "") {
            mostrarErro(campo, "Informe a idade.");
            return false;
        }
        limparErro(campo);
        return true;
    }

    function validarTelefone(campo) {
        var total = somenteDigitos(campo.value).length;
        if (total < 10) {
            mostrarErro(campo, "Informe o telefone com DDD. Ex.: (11) 99999-9999.");
            return false;
        }
        limparErro(campo);
        return true;
    }

    function configurarFormularioPaciente() {
        var form = document.getElementById("form-paciente");
        if (!form) { return; }

        var nome = document.getElementById("nome");
        var idade = document.getElementById("idade");
        var telefone = document.getElementById("telefone");

        aceitarSoDigitos(idade);
        aplicarMascara(telefone, formatarTelefone);

        // valida ao sair do campo e limpa o erro quando a pessoa volta a digitar
        [[nome, validarNome], [idade, validarIdade], [telefone, validarTelefone]].forEach(function (par) {
            par[0].addEventListener("blur", function () { par[1](par[0]); });
            par[0].addEventListener("input", function () { limparErro(par[0]); });
        });

        form.addEventListener("submit", function (evento) {
            // os três são validados (assim todos os erros aparecem de uma vez)
            var resultados = [validarNome(nome), validarIdade(idade), validarTelefone(telefone)];
            var tudoCerto = resultados.every(Boolean);

            if (!tudoCerto) {
                evento.preventDefault();
                var primeiroInvalido = form.querySelector(".campo-invalido");
                if (primeiroInvalido) { primeiroInvalido.focus(); }
            }
        });
    }

    /* ---------- filtro da tabela de pacientes ---------- */

    function configurarFiltroTabela() {
        var filtro = document.getElementById("filtro-tabela");
        var tabela = document.getElementById("tabela-pacientes");
        var aviso = document.getElementById("filtro-vazio");
        if (!filtro || !tabela) { return; }

        var linhas = tabela.querySelectorAll("tbody tr");

        filtro.addEventListener("input", function () {
            var termo = normalizar(filtro.value.trim());
            var visiveis = 0;

            linhas.forEach(function (linha) {
                var combina = termo === "" || normalizar(linha.textContent).indexOf(termo) !== -1;
                linha.hidden = !combina;
                if (combina) { visiveis += 1; }
            });

            if (aviso) { aviso.hidden = visiveis > 0; }
        });
    }

    /* ---------- início ---------- */

    if (typeof document !== "undefined") {  // só roda no navegador
        configurarFormularioPaciente();
        configurarFiltroTabela();
        aplicarMascara(document.getElementById("cpf"), formatarCpf);
    }

    // permite testar as funções de texto fora do navegador (Node)
    if (typeof module !== "undefined" && module.exports) {
        module.exports = { somenteDigitos: somenteDigitos, formatarTelefone: formatarTelefone,
                           formatarCpf: formatarCpf, normalizar: normalizar };
    }
})();
