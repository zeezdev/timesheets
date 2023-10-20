const api_host = process.env.TIMESHEET_API_HOST | 'localhost';
const api_url = `http://${api_host}:8874`;

module.exports = {
  "/api": {
    "target": api_url,
    "secure": false
  }
}
