document.querySelector(".start-btn").onclick = function(){

alert("Welcome to EduSphere! Start your learning journey 🚀");

};
function submitQuiz() {

    let answers = {};

    document.querySelectorAll(".question").forEach(q => {

        let id = q.querySelector("input").name;
        let selected = q.querySelector("input:checked");

        if (selected) {
            answers[id] = selected.value;
        }
    });

    fetch("/submit_quiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ answers })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            "Score: " + data.score + " / " + data.total;
    });
}