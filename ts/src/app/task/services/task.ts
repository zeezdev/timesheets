export interface Task {
  id?: number;
  name: string;
  category_id: number;
  category_name?: string;
  is_current?: number;
}
