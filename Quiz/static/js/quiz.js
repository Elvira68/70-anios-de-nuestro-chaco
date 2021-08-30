// const url = window.location.href

const timerBox  = document.getElementById("timer-box");
const respForm = document.getElementById("pregunta-form");


const activateTimer = (minutesParam, secondsParam) => {
    if (minutesParam.toString().length < 2) {
        timerBox.innerHTML = `<b>0${minutesParam}:${secondsParam}</b>`
    } else {
        timerBox.innerHTML = `<b>${minutesParam}:${secondsParam}</b>`
    }
    let minutes = minutesParam
    let seconds = secondsParam
    let displaySeconds
    let displayMinutes
    const timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                sendData()
                clearInterval(timer)
            }, 500)
        }
        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}

// Seteamos el cronómetro pasándole un valor entero que representan los minutos, y un valor entero que representan los segundos
activateTimer(0, 30)

const sendData = () => {
    respForm.submit(); 
}