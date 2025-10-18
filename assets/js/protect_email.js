// Protect email
const emailUsername = 'representantes.estudantes.fic';
const emailDomain = 'udc.gal';
const openEmail = () => {
    document.getElementById('email').href = `mailto:${emailUsername}@${emailDomain}`;
}
document.getElementById('email').setAttribute('onclick', 'openEmail();');