import os
import subprocess
import time
import select
import configparser
import time
import sys

timeout = 1

log = open("log.log", "w")
try:
    os.mkdir("logs-" + sys.argv[1])
except:
    pass
programs = []

programs = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(), default_section="")
programs.read("entrylist.ini")

stats = {}
test_data = [i.split() for i in open(sys.argv[1]).read().split("\n") if i.strip()]


def pad(s, l):
    return s + (l - len(s)) * " "


def print(*args, print=print, **kwargs):
    s = " ".join(str(i) for i in args)
    log.write(s + kwargs.get("end", "\n"))
    print(*args, **kwargs)


def compile(compiler, log):
    log.write("==> Compiling...\n")
    p = subprocess.Popen(compiler, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    try:
        stdout, stderr = p.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        p.kill()
    if stdout:
        log.write("==> STDOUT\n")
        log.write(stdout.decode("utf-8") + "\n")
    if stderr:
        log.write("==> STDERR\n")
        log.write(stderr.decode("utf-8") + "\n")
    if p.wait():
        log.write("==> Compiling failed\n")
        stats[name]["Errors"] += 1
        return False
    else:
        log.write("==> Compiling succeeded\n\n")
        return True


def test_q(ques, ans, runner, options, log):
    log.write("==> Input: '{}', expecting '{}'\n".format(ques, ans))
    inp = (ques + "\n").encode("utf-8") if not options.get("argv", fallback=False) else None
    r = runner if not options.get("argv", fallback=False) else runner + " " + ques
    p = subprocess.Popen(r, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    try:
        stdout, stderr = p.communicate(input=inp, timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        log.write("==> Timeout\n\n")
        return "Timeouts"

    if stderr:
        log.write("==> Stderr\n")
        log.write(stderr.decode("utf-8") + "\n")

    if stdout:
        raw_data = stdout.decode("utf-8")
        log.write("==> Stdout\n")
        log.write(raw_data + "\n")
        data = raw_data.strip().lower()

    retcode = p.wait()
    log.write("==> Return code {}\n".format(retcode))
    if retcode:
        log.write("==> Error\n\n")
        return "Errors"

    if data == ans.strip().lower():
        log.write("==> Pass\n\n")
        return "Passes"
    else:
        log.write("==> Fail\n\n")
        return "Fails"

print("Starting testing...")
print("Timeout:", timeout)
t = timeout * len(test_data)
ts = "(" + ":".join(map(str, divmod(t, 60))) + " minutes)"
print("Max", t, "seconds", ts, "per program")

for name, info in programs.items():
    if not name:
        continue
    print()
    with open("logs-" + sys.argv[1] + "/{}.log".format(name), "w") as nlog:
        print("Processing:", name)
        print("\tOptions:", ", ".join("{}: {}".format(i, j) for i, j in info.items() if i not in ("runner", "compiler")))

        stats[name] = {"Passes": 0, "Fails": 0, "Timeouts": 0, "Errors": 0}

        if info.get("compiler", fallback=""):
            print("\tCompiler command:", info["compiler"])
            print("\tCompiling...", end=" ", flush=True)
            if not compile(info["compiler"], nlog):
                print("FAIL")
                continue
            print("OK")

        print("\tRunner command:", info["runner"])
        print("\tRunning...", end=" ", flush=True)
        t = time.time()

        fails = set()

        for ans, ques in test_data:
            result = test_q(ques, ans, info["runner"], info, nlog)
            stats[name][result] += 1
            if result == "Fails":
                fails.add((ques, ans))
        t = time.time() - t

        nlog.write("==> Done!\n==> ")
        for key, value in sorted(stats[name].items()):
            nlog.write(pad("{}: {}/{}".format(key, value, len(test_data)), 20))
        nlog.write("\n")

        print("Done!")
        print("\tTook", t, "seconds,", t / len(test_data), "per test")
        nlog.write("==> Took " + str(t) + " seconds, " + str(t / len(test_data)) + " per test\n")
        nlog.write("==> Fails: " + str(fails) + "\n")

print()
print("Testing done!")
print("=" * 100)

for name, data in sorted(stats.items(), key=lambda i: -i[1]["Passes"]):
    print(pad(name + ":", 20), end="")
    for key, value in sorted(data.items()):
        print(pad("{}: {}/{}".format(key, value, len(test_data)), 20), end="")
    print()
