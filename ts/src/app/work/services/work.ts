export interface WorkReportByCategory {
  category: {
    id: number;
    name: string;
  },
  time: number;
}

export interface WorkReportByTask {
  task: {
    id: number;
    name: string;
    category: {
      id: number;
      name: string;
    },
  },
  time: number;
}

export interface WorkReportTotal {
  time: number;
}
