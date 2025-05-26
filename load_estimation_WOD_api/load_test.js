import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },   // ramp up to 10 users
    { duration: '1m', target: 10 },    // stay at 10 users
    { duration: '30s', target: 50 },   // ramp up to 50 users
    { duration: '1m', target: 50 },    // stay at 50 users
    { duration: '30s', target: 100 },  // ramp up to 100 users
    { duration: '1m', target: 100 },   // stay at 100 users
    { duration: '10s', target: 0 },    // ramp down
  ],
};

export default function () {
  const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYW5lLmRvZUBtYWlsLmNvbSIsIm5hbWUiOiJKYW5lIERvZSIsInJvbGUiOiJhZG1pbiIsImlzcyI6ImZpdC1hcGkiLCJpYXQiOjE3NDgyNjkzNTUsImV4cCI6MTc0ODI3MTE1NX0.0i9rK6oFJg5vJOf1vFgkM_GXWXgWH30-GHLdb3UjHs4';
  const res = http.get('http://localhost:5001/fitness/wod', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 5s': (r) => r.timings.duration < 5000,
  });

  sleep(1);
}
