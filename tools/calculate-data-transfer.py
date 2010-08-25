#!/usr/bin/python
import re
import sys

fileName = sys.argv[1]

compiledExpression = re.compile(".*\".*\" [-0-9]* ([0-9]*)")

fpFullLog = file(fileName)

totalBytes = 0

for line in fpFullLog:
  matches = compiledExpression.match(line)

  if matches is None:
    continue

  bytes = matches.group(1)

  if len(bytes) > 0: # avoid zero-length matches
    bytes = int(bytes)
    totalBytes += bytes

fpFullLog.close()

print "%.2f MiB" % (totalBytes/2.0**20)
