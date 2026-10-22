export interface Todo {
  id: number
  title: string
  completed: boolean
}

export interface TodoCreatePayload {
  title: string
}

export type TodoUpdatePayload = Partial<
  Pick<Todo, "title" | "completed">
>
