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
  return (
    <li
      key={todo.id}
      className={"flex items-center gap-2 bg-gray-50 p-3 rounded-lg border border-gray-200"}
    >
    <div className={`flex-1 flex items-center gap-2 ${
        todo.completed ? "line-through text-gray-400" : ""
      }`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
        className="cursor-pointer"
      />
      <span>{todo.title}</span>
    </div>
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
