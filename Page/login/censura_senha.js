function mostrarSenha(campo){
    seletorCampo=`#${campo}`

    let Campo = document.querySelector(seletorCampo)
    let imagemOlho = document.querySelectorAll('.icon__olho')

    if(Campo.type === 'password'){
        Campo.setAttribute('type','text');
        imagemOlho[0].setAttribute('src','../assets/olho_fechado.svg');
    } else {
        Campo.setAttribute('type','password');
        imagemOlho[0].setAttribute('src','../assets/olho.svg');
    }
}
