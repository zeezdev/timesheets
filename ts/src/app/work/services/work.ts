export interface WorkReportByCategory {
  category_id: number;
  category_name: string;
  time: number;
}

export interface WorkReportByTask {
  task_id: number;
  task_name: string;
  category_id: number;
  time: number;
}

export interface WorkReportTotal {
  time: number;
}
