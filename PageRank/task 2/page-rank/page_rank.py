import math

def page_rank(p, s, mp, lq, d):
    pr = list()
    newpr = list()
    perplexity=list()
    i = 0
    h=0
    perp=0
    n = len(p)
    while i < n:
        pr.append(1/n)
        newpr.append(1/n)
        i = i + 1
    x=0
    y=0
    while y < 4:
        h = convergence(pr)
        perpnew = pow(2,h)
        if perp-perpnew < 1:
            y += 1
        else:
            y=0
        perplexity.append(perpnew)
        perp=perpnew

        sinkpr = 0

        for j in s:
            sinkpr = sinkpr + pr[j]

        k = 0
        while k < n:

            newpr[k] = (1-d)/n
            newpr[k] = newpr[k] + (d * (sinkpr/n))
            for q in mp[k].split(" "):
                newpr[k] = newpr[k] + (d * pr[int(q)] / lq[int(q)])

            k=k+1

        l = 0
        while l < n:
            pr[l] = newpr[l]
            l = l+1
        x = x+1
    put_in_file(p, pr , perplexity)



def convergence(pr):
    i = 0
    h=0
    while i < len(pr):
        h = h + (pr[i] * math.log(pr[i], 2))
        i += 1

    return -h



def put_in_file(p, pr, perplexity):
    f = open("ranks.txt", "w")
    f.write("\n".join(reversed(sorted(map(lambda x, y: str(x) + "\t" + y, pr, p)))))
    f.close()

    f = open("perplexities.txt", "w")
    f.write("\n".join(map(lambda x: str(x), perplexity)))
    f.close()


pa = ["A", "B", "C", "D", "E", "F"]
sa = []
mpa = ["3 4 5", "0 5", "0 1 3", "1 2", "1 2 3 5", "0 1 3"]
lqa = [3, 4, 2, 4, 1, 3]

page_rank(pa,sa,mpa,lqa,0.85)
