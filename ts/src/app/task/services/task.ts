export interface Task {
  id?: number;
  name: string;
  category?: {
    id: number;
    name?: string;
  };
  is_current?: boolean;
  is_archived?: boolean;
}
