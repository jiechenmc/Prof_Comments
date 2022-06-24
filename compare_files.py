# Compare comments.tsv with route.tsv to ensure that every class was scraped
with open("data/routes.tsv", "r") as routes:
    routesTSV = routes.readlines()

with open("data/comments.tsv", "r") as comments:
    commentsTSV = comments.readlines()

for i, data in enumerate(routesTSV):
    comp1 = data.split()[1]
    comp2 = commentsTSV[i].split()[1]

    result = comp1 == comp2

    print(i, result)

    if not result:
        break