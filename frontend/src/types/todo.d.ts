export interface Todo {
  id: number
  title: string
  description: string
  completed: boolean
  favorite: boolean
}

export interface TodoCreatePayload {
  title: string
  description: string
}

export type TodoUpdatePayload = Partial<
  Pick<Todo, "title" | "description" | "completed" | "favorite">
>
