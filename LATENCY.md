
### Access JS variables
```python
print('average: ' + str(int(timeit.timeit(lambda: driver.execute_script("return game_state"), number=10000) / 10000 * 1000)) + 'ms')
# average: 4ms
```
