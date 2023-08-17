// Check if there are any todos stored in localStorage
let todos = localStorage.getItem('todos') ? JSON.parse(localStorage.getItem('todos')) : [];

// Display todos on page load
displayTodos();

// Add todo on button click
function addTodo() {
  const todoInput = document.getElementById('todo-input');
  const todoText = todoInput.value.trim();
  if (todoText !== '') {
    const todo = {
      id: new Date().getTime(),
      text: todoText,
      completed: false
    };
    todos.unshift(todo); // Add new todo at the beginning of the array
    localStorage.setItem('todos', JSON.stringify(todos));
    todoInput.value = '';
    displayTodos();
  }
}

// Display the todos and update progress bar
function displayTodos() {
  const todoList = document.getElementById('todo-list');
  todoList.innerHTML = '';
  let completedCount = 0;

  todos.forEach(function (todo) {
    const li = document.createElement('li');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = todo.completed;
    checkbox.addEventListener('change', function () {
      todo.completed = this.checked;
      localStorage.setItem('todos', JSON.stringify(todos));
      updateProgress();
      displayTodos();
    });

    const span = document.createElement('span');
    span.textContent = todo.text;
    if (todo.completed) {
      span.classList.add('completed');
    }
    span.addEventListener('dblclick', function () {
      const newText = prompt('Edit todo:', todo.text);
      if (newText !== null && newText.trim() !== '') {
        todo.text = newText.trim();
        localStorage.setItem('todos', JSON.stringify(todos));
        displayTodos();
      }
    });

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', function () {
      todos = todos.filter(item => item.id !== todo.id);
      localStorage.setItem('todos', JSON.stringify(todos));
      displayTodos();
    });

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(deleteButton);
    todoList.appendChild(li);

    if (todo.completed) {
      completedCount++;
    }
  });

  updateProgress(completedCount);
}

// Update the progress bar and percentage display
function updateProgress(completedCount) {
  const progressBar = document.querySelector('.progress-bar');
  const progressPercentage = document.querySelector('.progress-percentage');

  if (completedCount === undefined) {
    completedCount = todos.filter(todo => todo.completed).length;
  }

  const totalTodos = todos.length;
  const percentage = totalTodos === 0 ? 0 : Math.floor((completedCount / totalTodos) * 100);

  progressBar.style.width = percentage + '%';
  progressPercentage.textContent = percentage + '%';
}