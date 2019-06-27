import spell.metrics as metrics
import time
import random
import sys

if __name__ == "__main__":
  positive = 0
  num = 0
  step = 0
  for i in range(30):
    print("Step " + str(step) + ": " + str(i))
    metrics.send_metric("walk", i)
    step += 1
    time.sleep(1)
