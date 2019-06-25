import spell.metrics as metrics
import time
import random
import sys

if __name__ == "__main__":
  positive = 0
  num = 0
  step = 0
  for i in range(30):
    add = (random.random() - 0.5) * float(sys.argv[1])
    num += add
    positive += add
    positive = max(0, positive)
    print("Step " + str(step) + ": " + str(add) + " - num: " + str(num) + " - pos: " + str(positive))
    metrics.send_metric("pos_walk", positive)
    metrics.send_metric("walk", num)
    metrics.send_metric("text", "Hi! Number is " + str(num))
    step += 1
    time.sleep(1)
