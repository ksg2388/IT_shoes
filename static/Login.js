const id = document.getElementById('id')
const passward = document.getElementById('password')
const login = document.getElementById('login')
let errStack = 0;

login.addEventListener('click', () => {
    // 데이터 베이스 연결 전 임시 아이디 패스워드 입력
    if (id.value == 'acid') {
        if (password.value == '0000') {
            alert('로그인 되었습니다!')
        }
        else {
            alert('아이디와 비밀번호를 다시 한 번 확인해주세요!')
            errStack ++;
        }
    }
    else {
        alert('존재하지 않는 계정입니다.')
    }

    if (errStack >= 5) {
        alert('비밀번호를 5회 이상 틀리셨습니다. 비밀번호 찾기를 권장드립니다.')
    }
})