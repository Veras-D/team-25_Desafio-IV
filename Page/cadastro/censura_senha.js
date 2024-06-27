function mostrarSenha(campo,ordemNaLista){
    seletorCampo=`#${campo}`
    
    let Campo = document.querySelector(seletorCampo)
    let imagemOlho = document.querySelectorAll('.icon__olho')

    if(Campo.type === 'password'){
        Campo.setAttribute('type','text');
        imagemOlho[ordemNaLista].setAttribute('src','../assets/olho_fechado.svg');
    } else {
        Campo.setAttribute('type','password');
        imagemOlho[ordemNaLista].setAttribute('src','../assets/olho.svg');
    }
}