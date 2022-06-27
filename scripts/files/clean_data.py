with open("data.tsv", "r") as f:
    header = True

    for line in f:
        if header:
            header = False
            with open("final.tsv", "a+") as f:
                f.write(line)
            continue

        line = line.split("\t")
        line[6] = line[6].replace("\"grades\": ", "")
        line[5] = line[5].replace("{\"comments\":", "").replace(", }",
                                                                "").lstrip()

        line[6] = line[6].replace("{''}","[]")
        line[5] = line[5].replace("''}", "[]")

        line = "\t".join(line)
        with open("final.tsv", "a+") as f:
            f.write(line)