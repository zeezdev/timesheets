export function pad(num, size = 2) {
  return ('0' + num).substring(-size);
}
