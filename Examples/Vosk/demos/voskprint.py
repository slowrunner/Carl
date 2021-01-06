"""
File: voskprint.py

Pretty print for Vosk results

Result: 3 words
 0.28 carl
 1.00 wake
 1.00 up
Text: carl wake up

Usage:
from voskprint import printResult

printResult(rec.Result())
printResult(rec.FinalResult())

"""
import json

def printResult(res):
    jres = json.loads(res)
    if "result" in jres:
        jresult=jres["result"]
        # print(jresult)

        num_words = len(jresult)
        print("Result: {} words".format(num_words))

        for i in range(num_words):
            print("{:>5.2f} {:<s}".format(jresult[i]["conf"],jresult[i]["word"]))
        result_text = jres["text"]
        print("Text: {}".format(result_text))

