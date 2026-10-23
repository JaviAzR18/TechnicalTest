import React from "react";
import type { Todo } from "../types/todo";

interface TodoItemProps {
  todo: Todo;
  toggleTodo: (id: number) => void;
  removeTodo: (id: number) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  toggleTodo,
  removeTodo,
}) => {
  console.log(todo);
  return (
    <li className="flex items-start gap-3 bg-gray-50 p-3 rounded-lg border border-gray-200">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
        className="mt-1 cursor-pointer"
        aria-label={`Mark ${todo.title} as ${todo.completed ? "pending" : "completed"}`}
      />
      <div className="flex-1 min-w-0">
        <span
          className={`block font-medium ${
            todo.completed ? "line-through text-gray-400" : "text-gray-800"
          }`}
        >
          {todo.title}
        </span>
        {todo.description ? (
          <p
            className={`mt-1 text-sm ${
              todo.completed ? "text-gray-400" : "text-gray-600"
            }`}
          >
            {todo.description}
          </p>
        ) : null}
      </div>
      
      <button
        type="button"
        onClick={() => {}}
        className={`shrink-0 px-2 py-1 rounded-lg transition cursor-pointer ${
          todo.favorite
            ? "text-amber-500 hover:bg-amber-50"
            : "text-gray-400 hover:bg-gray-100"
        }`}
      >
        {todo.favorite ? "★" : "☆"}
      </button>

      <button
        type="button"
        onClick={() => removeTodo(todo.id)}
        className="shrink-0 bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg transition cursor-pointer text-sm"
      >
        Delete
      </button>
    </li>
  );
};

export default TodoItem;
