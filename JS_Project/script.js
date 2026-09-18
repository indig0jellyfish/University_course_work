let form = document.querySelector("#form")
let input = document.querySelector("#task")
let list = document.querySelector("#list")
let tasks = localStorage.getItem("tasks")

if (tasks) {
    tasks = JSON.parse(tasks)
} else {
    tasks = []
}

const save = () => {
    localStorage.setItem("tasks", JSON.stringify(tasks))
}

const render = () => {
    list.innerHTML = ""

    for (let i = 0; i < tasks.length; i++) {
        let li = document.createElement("li")

        li.textContent = tasks[i] + " "

        let editBtn = document.createElement("button")
        editBtn.textContent = "Edit"

        let delBtn = document.createElement("button")
        delBtn.textContent = "Delete"

        delBtn.addEventListener("click", () => {
            tasks.splice(i, 1)
            save()
            render()
        })

        editBtn.addEventListener("click", () => {
            let editInput = document.createElement("input")
            editInput.value = tasks[i]

            let saveBtn = document.createElement("button")
            saveBtn.textContent = "Save"

            li.innerHTML = ""
            li.appendChild(editInput)
            li.appendChild(saveBtn)

            saveBtn.addEventListener("click", () => {
                tasks[i] = editInput.value
                save()
                render()
            })
        })

        li.appendChild(editBtn)
        li.appendChild(delBtn)

        list.appendChild(li)
    }
}

form.addEventListener("submit", (e) => {
    e.preventDefault()

    if (input.value === "") return

    tasks.push(input.value)
    save()
    render()

    input.value = ""
})

render()