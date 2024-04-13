
// let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    // menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};

let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');

window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if (top >= offset && top < offset + height) {
            navLinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            });
        };

    });

    let header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 100);

    // Remover NAVBAR ICONE quando clicar no navbar

    // menuIcon.classList.remove('bx-x');
    navbar.classList.remove('active');
};

// ScrollReveal({
//     // reset: true,
//     distance: '80px',
//     duration: 2000,
//     delay: 100
// });

// ScrollReveal().reveal('.home-content, .heading, .txt', { origin: 'top' });
// ScrollReveal().reveal('.contact form, .card, .info-text p', { origin: 'bottom' });
// ScrollReveal().reveal('.container-solucoes ul li:nth-last-child(odd)', { origin: 'left' });
// ScrollReveal().reveal('.container-solucoes ul li:nth-last-child(even)', { origin: 'right' });

// // Typed js text

// const typed = new Typed('.multiple-text', {
//     strings: ['Projetos', 'Pesquisas', 'Estudos'],
//     typeSpeed: 100,
//     backSpeed: 100,
//     typeDelay: 2000,
//     loop: true

// });

// window.onbeforeunload = () => {
//     for (const form of document.getElementsByTagName('form')) {
//         form.reset();
//     }
// }

// document.getElementById("criar-conta-btn").addEventListener("click", function () {
//     var email = document.getElementById("email").value;
//     localStorage.setItem("email", email);
// });


// function verificaEmailCadastrado() {
//     var email = document.getElementById("email").value;

//     fetch(`http://localhost:3000/usuarios/verificaEmail/${email}`, {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//         .then(response => {
//             // Verifica se a resposta da requisição é bem sucedida
//             if (response.ok) {
//                 // Se sim, retorna o resultado em formato JSON
//                 return response.json();
//             } else {
//                 // Se não, lança um erro
//                 throw new Error('Erro ao verificar e-mail');
//             }
//         })
//         .then(result => {
//             // Verifica se há pelo menos um registro retornado pela consulta
//             if (result.response.length > 0) {
//                 // Se sim, emite um alerta indicando que o e-mail já está cadastrado
//                 alert('O e-mail informado já está cadastrado. Faça o login ou use outro e-mail para se cadastrar.');
//             } else {
//                 // Se não, redireciona o usuário para a página de cadastro
//                 window.location.href = "../ScreenRegister/acesso-index.html";
//             }
//         })
//         .catch(error => {
//             // Trata erros na requisição ou no processamento do resultado
//             console.error('Erro ao verificar e-mail', error);
//             alert('Ocorreu um erro ao verificar o e-mail. Tente novamente mais tarde.');
//         });
// }


// // modificar a cor de plano de fundo

// const backgroundLogin = localStorage.getItem("corScreen");
// if (backgroundLogin === "1") {
//     document.body.classList.add("light-theme");
//     console.log("O valor de backgroundLogin é 1.");
// } else {
//     document.body.classList.remove("light-theme");
//     console.log("O valor de backgroundLogin é diferente de 1.");
// }