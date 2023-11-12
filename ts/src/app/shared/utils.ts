import {defer, Observable} from "rxjs";
import {HttpErrorResponse} from "@angular/common/http";

export function pad(num: number, size: number = 2, char: string = '0'): string {
  /**
   * Convert a given number to a string with zero-fill padding.
   * @param num A number to converto to a string.
   * @param size A number of zero characters in padding.
   * @param char A character to fill the string.
   */
  return String(num).padStart(size, char);
}

/**
 * Create async observable error that errors
 * after a JS engine turn
 */
export function asyncError<T>(errorObject: any) {
  return defer(() => Promise.reject(errorObject));
}

/**
 * Handle Http operation that failed.
 * Let the app continue.
 *
 * @param operation - name of the operation that failed
 */
export function handleError<T>(operation = 'operation') {
  return (error: HttpErrorResponse): Observable<T> => {
    // TODO: send the error to remote logging infrastructure
    console.error(error); // log to console instead

    // If a native error is caught, do not transform it. We only want to
    // transform response errors that are not wrapped in an `Error`.
    if (error.error instanceof Event) {
      throw error.error;
    }

    const message = `server returned code ${error.status} with body "${error.error}"`;
    // TODO: better job of transforming error for user consumption
    throw new Error(`${operation} failed: ${message}`);
  };
}
