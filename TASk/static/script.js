const api = "/tasks"

function loadTasks(){

fetch(api)
.then(res => res.json())
.then(data => {

const list = document.getElementById("taskList")
list.innerHTML=""

data.forEach(task => {

const li = document.createElement("li")

li.innerHTML = `
${task.title} - ${task.description}
<button onclick="deleteTask(${task.id})">Delete</button>
`

list.appendChild(li)

})

})
}

function addTask(){

const title = document.getElementById("title").value
const desc = document.getElementById("desc").value

fetch(api,{
method:"POST",
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
title:title,
description:desc
})
})
.then(()=>loadTasks())
}

function deleteTask(id){

fetch(api+"/"+id,{
method:"DELETE"
})
.then(()=>loadTasks())

}

loadTasks()