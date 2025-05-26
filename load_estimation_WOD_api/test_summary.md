# Load Test Report: WOD API

## Objective
Estimate the number of concurrent users the `/fitness/wod` API can support before exceeding a 5-second response time.

---

## Test Tool

- **Tool:** [k6](https://k6.io/)
- **Script Language:** JavaScript
- **Command Used:**
  ```bash
  k6 run load_test.js
  ```

---

## Test Configuration

Staged test using the following setup:

```javascript
export const options = {
  stages: [
    { duration: "30s", target: 10 },
    { duration: "30s", target: 25 },
    { duration: "30s", target: 50 },
    { duration: "1m",  target: 100 },
    { duration: "30s", target: 50 },
    { duration: "30s", target: 25 },
    { duration: "30s", target: 0 },
  ]
};
```

Each Virtual User (VU) sent repeated requests to `/fitness/wod`.

---

## Results Summary

| Metric                        | Value              |
|------------------------------|--------------------|
| Total Requests               | 1,015              |
| Successful Responses (200)   | 100%               |
| Responses < 5s               | 11%                |
| Avg Response Time            | 13.27s             |
| 95th Percentile Response Time| 23.26s             |

---

## Conclusion

- The API **works best with 10–15 concurrent users** if response time < 5s is required.
- Performance degrades significantly above this threshold due to CPU-bound logic (`heavy_computation()`).
- Consider **refactoring or optimizing the WOD generation** for better scalability.