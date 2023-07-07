export function pad(num: number, size: number = 2): string {
  /**
   * Convert a given number to a sring with zero-fill padding.
   * @param num A number to converto to a string.
   * @param size A number of zero characters in padding.
   */
  return ('0' + num).substring(-size);
}
