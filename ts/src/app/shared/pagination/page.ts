import { Observable } from 'rxjs';

export interface Sort<T> {
  property: keyof T;
  order: 'asc' | 'desc';
}

export interface PageRequest<T> {
  page: number;
  size: number;
  sort?: Sort<T>;
}

export interface Page<T> {
  items: T[]; // Objects of the current page.
  total: number; // The total count of objects.
  size: number; // The current page size.
  page: number; // The current page index.
  pages: number; // The total count of pages.
}

export type PaginatedEndpoint<T, Q> = (pageable: PageRequest<T>, query: Q) => Observable<Page<T>>
