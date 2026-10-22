import type { Todo, TodoCreatePayload, TodoUpdatePayload } from "../types/todo";

const BASE_URL = "http://localhost:8000/todos";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    throw new Error(`Request failed with status ${res.status}`);
  }
  if (res.status === 204) {
    return undefined as T;
  }
  console.log(res);
  return res.json();
}

export const getTodos = async (): Promise<Todo[]> => {
  const res = await fetch(BASE_URL);
  return handleResponse<Todo[]>(res);
};

export const createTodo = async (payload: TodoCreatePayload): Promise<Todo> => {
  const res = await fetch(BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...payload,
      completed: false,
    }),
  });
  return handleResponse<Todo>(res);
};

export const updateTodo = async (
  id: number,
  payload: TodoUpdatePayload
): Promise<Todo> => {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  console.log(res);
  return handleResponse<Todo>(res);
};

export const deleteTodo = async (id: number): Promise<void> => {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: "DELETE",
  });
  await handleResponse<void>(res);
};
