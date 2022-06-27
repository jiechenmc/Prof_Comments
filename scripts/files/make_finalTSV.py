with open("./_missing_comments.tsv", "r") as f:
    m_comments = f.readlines()

with open("./_comments.tsv", "r") as comments:
    for line in comments:
        line = line.split()
        for r in m_comments:
            if line[:5] == r.split()[:5]:
                with open("./_FINAL_COMMENTS.tsv", "a+") as f:
                    f.write(r)
                break
            else:
                with open("./_FINAL_COMMENTS.tsv", "a+") as f:
                    f.write("\t".join(line) + "\n")
                break