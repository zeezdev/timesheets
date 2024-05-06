import {Observable} from "rxjs";

export interface WorkItem {
  id?: number;
  task_id: number;
  start_dt: Date;
  end_dt?: Date;
}


// /**
//  * TODO: Move to shared location
//  */
// export interface PaginatedResponse<Type> {
//   items: [Type];
//   page: number;
//   size: number;
//   pages: number;
//   total: number;
// }
