let lgpdurl = 'https://jsonplaceholder.typicode.com/posts'; // URL do servidor/banco de dados para gerar o id do usuário.
let lgpdHtml = `
    <div class="lgpd">
      <div style="text-align:left">
        Ultilizamos cookies para melhorar a experiência do usuário. Clique em Aceitar para consentir a utilização dos
        cookies e para mais informações visite a nossa <a href="privacidade" target="_blank">Politica de privacidade.</a><!--colocar link da politica de qualidade -->
      </div>
      <div style="margin-top: 3px;">
        <button>ACEITAR</button>
      </div>
    </div>    
    <link rel="stylesheet" href="{{ url_for('static', filename='estilo.css') }}">
`
let lscontent = localStorage.getItem('lgpd')
if(!lscontent) {
    document.body.innerHTML += lgpdHtml; // faz a verificação se o usuário aceitou os termos.

    let lgpdArea = document.querySelector('.lgpd')
    let lgpdButton = lgpdArea.querySelector('Button')

    lgpdButton.addEventListener('click', async ()=>{
        lgpdArea.remove(); // faz a remoçao da identificação do usuário.

        let result = await fetch(lgpdurl); // Chamada para um servidor para coletar a id do usuário que entrou no site e gerar um código único para o usuário.
        let json = await result.json();

        if(json.error != '') {
            let id = '123'; // somente para teste.
            localStorage.setItem('lgpd', json.id); // Salva a id/código do usuário.
        }
    })
}
