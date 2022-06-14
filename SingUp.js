const singUp = document.getElementById('singUp')

function checkSingUp() {
    let id = document.getElementById('id').value
    let name = document.getElementById('name').value
    let passward = document.getElementById('password').value
    let passwardConfirm = document.getElementById('passwordConfirm').value
    let check = true;

    if (id === "") {    //id가 공백인 경우 오류 처리
        document.getElementById("idError").innerHTML="아이디를 입력해주세요"
        check = false
    }

    if (name === "") {  //닉네임이 공백인 경우 오류 처리
        document.getElementById("nameError").innerHTML="닉네임을 압력해주세요"
        check = false
    }

    if (passward === "") {  //비밀번호가 공백인 경우 오류 처리
        document.getElementById("passwordError").innerHTML="비밀번호를 압력해주세요"
        check = false
    }

    if (passwardConfirm !== passward) {  //비밀번호가 다를 경우
        document.getElementById("passwordConfirmError").innerHTML="비밀번호를 다시 확인해주세요"
        check = false
    }

    if (check) {
        document.getElementById("idError").innerHTML=""
        document.getElementById("nameError").innerHTML=""
        document.getElementById("passwordError").innerHTML=""
        document.getElementById("passwordConfirmError").innerHTML=""

        setTimeout(function() {
            alert("회원가입이 완료되었습니다")
        }, 0);
    }
}