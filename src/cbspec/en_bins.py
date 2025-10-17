import matplotlib.pyplot as plt
import config


def en_bins(infile):
    herec = plt.hist(infile[0], bins=config.ENERGYRANGE)
    hedt = plt.hist(infile[1], bins=config.ENERGYRANGE)
    hethr = plt.hist(infile[2], bins=config.ENERGYRANGE)

    ratio_logens = []
    N_logens = []
    nr = []
    nt = []
    log10en = []
    for i in range(len(herec[0])):
        if hethr[0][i] > 1 and hethr[1][i] > config.COENERGY:
            r = herec[0][i]
            nr.append(r)
            t = hethr[0][i]
            nt.append(t)
            d = r / t
            n = hedt[0][i]
            ratio_logens.append(d)
            N_logens.append(n)
            log10en.append(hedt[1][i])

    return log10en, N_logens, ratio_logens