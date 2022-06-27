# Pull out the routes for those classes with no comments
# To ensure data was accurate
with open("./_routes.tsv", "r") as routes:
    routesTSV = routes.readlines()
with open("./_no_comments.tsv", "r") as comments:
    for line in comments:
        line = line.split()
        for r in routesTSV:
            if line[:5] == r.split()[:5]:
                with open("./_no_comment_routes.tsv", "a+") as f:
                    f.write(r)
                break
