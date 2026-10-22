// src/App.tsx
import { useState, useEffect, useCallback  } from "react";
import type { Todo } from "./types/todo";
import { createTodo, deleteTodo , getTodos, updateTodo } from "./api/todo.ts";
import TodoForm from "./components/TodoForm";
import TodoList from "./components/TodoList";

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);

  
  const loadTodos = useCallback(async () => {
  try {
    const data = await getTodos();
    setTodos(data);
    setError(null);
    } catch {
      setError("Could not load tasks. Make sure the backend is running.");
    }
  }, []);
  useEffect(() => {
    void loadTodos();
  }, [loadTodos]);
  
  
  const addTodo = async () => {
    if (!title.trim()) return;
    try {
      await createTodo({
        title: title.trim(),
      });
      setTitle("");
      await loadTodos();
    } catch {
      setError("Could not create the task.");
    }
  };

  const toggleTodo = async (id: number) => {
    const todo = todos.find((item) => item.id === id);
    if (!todo) return;
    try {
      await updateTodo(id, { completed: !todo.completed });
      await loadTodos();
    } catch {
      setError("Could not update the task status.");
    }
  };

  const removeTodo = async (id: number) => {
    try {
      await deleteTodo(id);
      await loadTodos();
    } catch {
      setError("Could not delete the task.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-4 text-gray-800">ToDo List</h1>

        <TodoForm
          title={title}
          setTitle={setTitle}
          addTodo={addTodo}
        />

        {error ? (
          <p className="mb-4 text-sm text-red-600" role="alert">
            {error}
          </p>
        ) : null}

        <section>
          <h2 className="text-lg font-semibold mb-3 text-gray-800">Tasks</h2>
          <TodoList
            todos={todos}
            emptyMessage="No tasks yet."
            toggleTodo={toggleTodo}
            removeTodo={removeTodo}
          />
        </section>
      </div>
    </div>
  );
}

export default App;
