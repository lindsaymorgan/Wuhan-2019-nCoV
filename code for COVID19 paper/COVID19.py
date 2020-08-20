import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import logbin as lb
import glob
from scipy.optimize import fsolve
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from scipy.interpolate import splev
from scipy.interpolate import splrep
import colorsys
import networkx as nx
import random
import math
import matplotlib.style
import matplotlib as mpl
import csv
  

def show_recovery_rate():
    plt.figure(figsize=(12,10))
    lag = 1

    ### load data China
    data_con = []
    with open('/home/bnaya/Desktop/COVID19/city-confirmed-pivot-day-summary-2020-03-29.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_con.append(row)

    data_dead = []
    with open('/home/bnaya/Desktop/COVID19/city-dead-pivot-day-summary-2020-03-29.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_dead.append(row)

    data_recovered = []
    with open('/home/bnaya/Desktop/COVID19/city-cured-pivot-day-summary-2020-03-29.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_recovered.append(row)

    cl = 0
    for row_idx in range(len(data_con[1:])):
        row = data_con[1:][row_idx]
        row_rec = data_recovered[1:][row_idx]
        row_dead = data_dead[1:][row_idx]
        splited = row[0].split(',')
        splited_rec = row_rec[0].split(',')
        splited_dead = row_dead[0].split(',')

        if float(splited_rec[-3]) < 2000: # keep cities with enough statistics
            continue

        for jj in range(len(splited)):
            if len(splited[jj]) != 0:
                idx = jj
                break

        a = [float(s) for s in splited[idx:-2]]
        dead = [float(s) for s in splited_dead[-(len(a) + 2):-2]]
        recovered = [float(s) for s in splited_rec[-(len(a) + 2):-2]]



        rate = []
        time = []
        new_rec = []
        real_i = []

        # calculate the rate
        for i in range(lag, len(a)):
            if (a[i - lag] - (dead[i - lag] + recovered[i - lag])) == 0:
                continue
            rate.append((recovered[i] - recovered[i - 1]) / (a[i - lag] - (dead[i - lag] + recovered[i - lag])))
            new_rec.append(recovered[i] - recovered[i - 1])
            real_i.append(a[i - lag] - (dead[i - lag] + recovered[i - lag]))
            rate[-1] = rate[-1]/lag
            time.append(i)

        new_x2 = []
        new_y2 = []
        for w in range(len(rate)):
            if rate[w] > 0:
                new_x2.append(time[w])
                new_y2.append(rate[w])

        new_x3 = []
        new_y3 = []

        ddd = 3
        for i in range(ddd, len(new_x2) - ddd):
            if ddd == 0:
                new_x3.append(np.mean(new_x2[i]))
                new_y3.append(np.mean(new_y2[i]))
            else:
                new_x3.append(np.mean(new_x2[i - ddd:i + ddd]))
                new_y3.append(np.mean(new_y2[i - ddd:i + ddd]))

        yy = new_y3
        xx = new_x3

        new_x = []
        new_y = []

        for w in range(len(xx)):
            if yy[w] > 0:
                new_x.append(xx[w])
                new_y.append(yy[w])
        new_y = np.log10(new_y)

        m, bb = np.polyfit(new_x, new_y, 1)

        plt.semilogy(new_x3, new_y3, 'o', color='white', mec=cm.cool(cl / 3), mew=3, linewidth=2, ms=8, label=splited_rec[-1] + " - China" + r'$,k = $' + str(m)[:5])
        temp = [10 ** (m * xr + bb) for xr in new_x]
        plt.plot(new_x, temp, '--', color=cm.cool(cl / 3), linewidth=3)
        cl = cl + 1




    ### load data Italy
    data_con = []
    with open('/home/bnaya/Desktop/COVID19/confirmed_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_con.append(row)

    data_dead = []
    with open('/home/bnaya/Desktop/COVID19/dead_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_dead.append(row)

    data_recovered = []
    with open('/home/bnaya/Desktop/COVID19/cured_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_recovered.append(row)

    cl = 0
    color_list = ['r', 'b', 'g']
    for row_idx in range(3):
        row = data_con[1:][row_idx]
        row_rec = data_recovered[1:][row_idx]
        row_dead = data_dead[1:][row_idx]
        splited = row[0].split(',')
        splited_rec = row_rec[0].split(',')
        splited_dead = row_dead[0].split(',')

        if float(splited_dead[-3]) < 150: # keep cities with enough statistics
            continue

        for jj in range(len(splited)):
            if len(splited[jj]) != 0:
                idx = jj
                break

        a = [float(s) for s in splited[idx:-1]]
        dead = [float(s) for s in splited_dead[idx:-1]]
        recovered = [float(s) for s in splited_rec[idx:-1]]

        rate = []
        time = []


        # calculate the rate
        for i in range(lag, len(a)):
            if (a[i - lag] - (dead[i - lag] + recovered[i - lag])) == 0:
                continue
            rate.append((recovered[i] - recovered[i - 1]) / (a[i - lag] - (dead[i - lag] + recovered[i - lag])))
            rate[-1] = rate[-1]/lag
            time.append(i + 8)   #8 days of data  after China

        new_x2 = []
        new_y2 = []
        for w in range(len(rate)):
            if rate[w] > 0:
                new_x2.append(time[w])
                new_y2.append(rate[w])

        new_x3 = []
        new_y3 = []

        ddd = 3
        for i in range(ddd, len(new_x2) - ddd):
            if ddd == 0:
                new_x3.append(np.mean(new_x2[i]))
                new_y3.append(np.mean(new_y2[i]))
            else:
                new_x3.append(np.mean(new_x2[i - ddd:i + ddd]))
                new_y3.append(np.mean(new_y2[i - ddd:i + ddd]))


        if cl == 1:
            splited_dead[-1] = "Emilia Romagna"
            plt.semilogy(new_x3, new_y3, 'o', color = color_list[cl], label = splited_dead[-1] + " - Italy", mec = color_list[cl], linewidth = 2, ms = 8, mew = 3)
        else:
            plt.semilogy(new_x3, new_y3, 'o', color = color_list[cl], label = splited_dead[-1] + " - Italy", mec = color_list[cl], linewidth = 2, ms = 8, mew = 3)

        cl = cl + 1

    plt.tick_params(labelsize=25)
    plt.legend(loc='upper left', ncol = 1, fontsize=18)
    plt.xlim([0,60])
    plt.ylabel(r'$P_{recovery}(t)$', fontsize=32)
    plt.xlabel("Days from first infection", fontsize=32)
    plt.tight_layout()

def show_death_rate():
    plt.figure(figsize=(12,10))
    lag = 1


    ## load data China
    data_con = []
    with open('/home/bnaya/Desktop/COVID19/city-confirmed-pivot-day-summary-2020-03-29.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_con.append(row)

    data_dead = []
    with open('/home/bnaya/Desktop/COVID19/city-dead-pivot-day-summary-2020-03-29.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_dead.append(row)

    data_recovered = []
    with open('/home/bnaya/Desktop/COVID19/city-cured-pivot-day-summary-2020-03-29.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_recovered.append(row)

    cl = 0
    for row_idx in range(len(data_con[1:])):
        row = data_con[1:][row_idx]
        row_rec = data_recovered[1:][row_idx]
        row_dead = data_dead[1:][row_idx]
        splited = row[0].split(',')
        splited_rec = row_rec[0].split(',')
        splited_dead = row_dead[0].split(',')


        if float(splited_dead[-3]) < 150: # keep cities with enough statistics
            continue


        for jj in range(len(splited)):
            if len(splited[jj]) != 0:
                idx = jj
                break

        a = [float(s) for s in splited[idx:-2]]
        dead = [float(s) for s in splited_dead[-(len(a) + 2):-2]]
        recovered = [float(s) for s in splited_rec[-(len(a) + 2):-2]]

        rate = []
        time = []

        # calculate rate
        for i in range(lag, len(a)):
            if (a[i - lag] - (dead[i - lag] + recovered[i - lag])) == 0:
                continue
            rate.append((dead[i] - dead[i - 1]) / (a[i - lag] - (dead[i - lag] + recovered[i - lag])))
            rate[-1] = rate[-1]/lag
            time.append(i)

        new_x2 = []
        new_y2 = []
        for w in range(len(rate)):
            if rate[w] > 0:
                new_x2.append(time[w])
                new_y2.append(rate[w])

        new_x3 = []
        new_y3 = []

        ddd = 1
        for i in range(ddd, len(new_x2) - ddd):
            if ddd == 0:
                new_x3.append(np.mean(new_x2[i]))
                new_y3.append(np.mean(new_y2[i]))
            else:
                new_x3.append(np.mean(new_x2[i - ddd:i + ddd]))
                new_y3.append(np.mean(new_y2[i - ddd:i + ddd]))

        yy = new_y3[:-27]
        xx = new_x3[:-27]

        new_x = []
        new_y = []

        for w in range(len(xx)):
            if yy[w] > 0:
                new_x.append(xx[w])
                new_y.append(yy[w])
        new_y = np.log10(new_y)

        m, bb = np.polyfit(new_x, new_y, 1)
        tau = -1 / m
        if splited_dead[-1] == "Wuhan":
            plt.semilogy(new_x3, new_y3, 'o', color='white', mec=cm.cool(cl / 2), mew=3, linewidth=2, ms=8,
                         label=splited_dead[-1] + " - China" + r'$, \tau = $' + str(tau)[:4])
            temp = [10**(m*xr + bb) for xr in new_x]
            plt.plot(new_x, temp, '--', color = cm.cool(cl / 2), linewidth = 3)
        else:
            plt.semilogy(new_x3, new_y3, 'o', color='white', mec=color_list[cl], mew=3, linewidth=2, ms=8,
                     label=splited_dead[-1])
        cl = cl + 1

    ## load data Italy
    data_con = []
    with open('/home/bnaya/Desktop/COVID19/confirmed_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_con.append(row)

    data_dead = []
    with open('/home/bnaya/Desktop/COVID19/dead_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_dead.append(row)

    data_recovered = []
    with open('/home/bnaya/Desktop/COVID19/cured_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_recovered.append(row)

    cl = 0
    color_list = ['r','g','b']
    for row_idx in range(3):
        row = data_con[1:][row_idx]
        row_rec = data_recovered[1:][row_idx]
        row_dead = data_dead[1:][row_idx]
        splited = row[0].split(',')
        splited_rec = row_rec[0].split(',')
        splited_dead = row_dead[0].split(',')

        if float(splited_dead[-3]) < 150: # keep cities with enough statistics
            continue


        for jj in range(len(splited)):
            if len(splited[jj]) != 0:
                idx = jj
                break

        a = [float(s) for s in splited[idx:-1]]
        dead = [float(s) for s in splited_dead[idx:-1]]
        recovered = [float(s) for s in splited_rec[idx:-1]]

        rate = []
        time = []

        # calculate rate
        for i in range(lag, len(a)):
            if (a[i - lag] - (dead[i - lag] + recovered[i - lag])) == 0:
                continue
            rate.append((dead[i] - dead[i - 1]) / (a[i - lag] - (dead[i - lag] + recovered[i - lag])))
            rate[-1] = rate[-1]/lag
            time.append(i+8) #8 days of data  after China

        new_x2 = []
        new_y2 = []
        for w in range(len(rate)):
            if rate[w] > 0:
                new_x2.append(time[w])
                new_y2.append(rate[w])

        new_x3 = []
        new_y3 = []

        ddd = 1
        for i in range(ddd, len(new_x2) - ddd):
            if ddd == 0:
                new_x3.append(np.mean(new_x2[i]))
                new_y3.append(np.mean(new_y2[i]))
            else:
                new_x3.append(np.mean(new_x2[i - ddd:i + ddd]))
                new_y3.append(np.mean(new_y2[i - ddd:i + ddd]))


        yy = new_y3[20:]
        xx = new_x3[20:]

        new_x = []
        new_y = []

        for w in range(len(xx)):
            if yy[w] > 0:
                new_x.append(xx[w])
                new_y.append(yy[w])
        new_y = np.log10(new_y)

        m, bb = np.polyfit(new_x, new_y, 1)
        tau = -1 / m

        if cl == 1:
            splited_dead[-1] = "Emilia Romagna"

        plt.semilogy(new_x3, new_y3, 'o', color = color_list[cl], label = splited_dead[-1] + " - Italy"  + r'$, \tau = $' + str(tau)[:4], mec = color_list[cl], linewidth = 2, ms = 8, mew = 3)
        temp = [10 ** (m * xr + bb) for xr in new_x]
        plt.plot(new_x, temp, '--', color=color_list[cl], linewidth=3)

        cl = cl + 1

    plt.tick_params(labelsize=25)
    plt.legend(loc='lower left', fontsize=18)
    plt.xlim([0,60])
    plt.ylabel(r'$P_{death}(t)$', fontsize=32)
    plt.xlabel("Days from first infection", fontsize=32)
    plt.tight_layout()


def show_infection_rate_china_italy():
    plt.figure(figsize=(10, 8))


    #load data Italy
    data_con = []
    with open('/home/bnaya/Desktop/COVID19/confirmed_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_con.append(row)

    data_dead = []
    with open('/home/bnaya/Desktop/COVID19/dead_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_dead.append(row)

    data_recovered = []
    with open('/home/bnaya/Desktop/COVID19/cured_italy.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_recovered.append(row)


    color_list = ['r','g','b']
    cl = 0
    for row_idx in range(len(data_con[1:])):
        row = data_con[1:][row_idx]
        row_rec = data_recovered[1:][row_idx]
        row_dead = data_dead[1:][row_idx]
        splited = row[0].split(',')
        splited_rec = row_rec[0].split(',')
        splited_dead = row_dead[0].split(',')


        for jj in range(len(splited)):
            if len(splited[jj]) != 0:
                idx = jj
                break

        a = [float(s) for s in splited[idx:-2]]
        dead = [float(s) for s in splited_dead[-(len(a) + 2):-2]]
        recovered = [float(s) for s in splited_rec[-(len(a) + 2):-2]]

        rate = []
        time = []


        # calculate rate
        l = 1
        for i in range(1 + l - 1, len(a)):
            if (a[i - l] - (recovered[i - l] + dead[i - l])) == 0:
                continue
            else:
                rate.append((a[i] - a[i - 1]) / (a[i - l] - (recovered[i - l] + dead[i - l])))
                time.append(i + 8)

        new_x = []
        new_y = []

        yy = rate[10:]
        xx = time[10:]

        if cl == 1:
            yy = rate[10:]
            xx = time[10:]

        for w in range(len(xx)):
            if yy[w] > 0:
                new_x.append(xx[w])
                new_y.append(yy[w])
        new_y = np.log10(new_y)

        new_x2 = []
        new_y2 = []
        for w in range(len(rate)):
            if rate[w] > 0:
                new_x2.append(time[w])
                new_y2.append(rate[w])

        m, bb = np.polyfit(new_x, new_y, 1)
        tau = -1 / m
        if cl == 1:
            splited_rec[-1] = "Emilia Romagna"
        plt.semilogy(new_x2, new_y2, 'o', color=color_list[cl],
                     label=splited_rec[-1] + " - Italy" + r'$, \tau = $' + str(tau)[:4], mec=color_list[cl],
                     linewidth=2, ms=8, mew=3)

        temp = [10 ** (m * xr + bb) for xr in new_x]
        plt.plot(new_x, temp, '--', color=color_list[cl], linewidth=3)
        cl = cl + 1



    #load data China
    data_con = []
    with open('/home/bnaya/Desktop/COVID19/city-confirmed-pivot-day-summary-2020-04-27.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_con.append(row)

    data_dead = []
    with open('/home/bnaya/Desktop/COVID19/city-dead-pivot-day-summary-2020-04-27.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_dead.append(row)

    data_recovered = []
    with open('/home/bnaya/Desktop/COVID19/city-cured-pivot-day-summary-2020-04-27.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_recovered.append(row)

    cl = 0
    for row_idx in range(len(data_con[1:])):
        row = data_con[1:][row_idx]
        row_rec = data_recovered[1:][row_idx]
        row_dead = data_dead[1:][row_idx]
        splited = row[0].split(',')
        splited_rec = row_rec[0].split(',')
        splited_dead = row_dead[0].split(',')

        if splited[-1] not in ["Beijing", "Shanghai", "Guangzhou"]:
            continue

        for jj in range(len(splited)):
            if len(splited[jj]) != 0:
                idx = jj
                break

        a = [float(s) for s in splited[idx:-2]]
        dead = [float(s) for s in splited_dead[-(len(a) + 2):-2]]
        recovered = [float(s) for s in splited_rec[-(len(a) + 2):-2]]

        rate = []
        time = []


        #calculate rate
        l = 1
        for i in range(1 + l - 1, len(a)):
            if (a[i - l] - (recovered[i - l] + dead[i - l])) == 0:
                continue
            else:
                rate.append((a[i] - a[i - 1]) / (a[i - l] - (recovered[i - l] + dead[i - l])))
                time.append(i)

        new_x2 = []
        new_y2 = []
        for w in range(len(rate)):
            if rate[w] > 0:
                new_x2.append(time[w])
                new_y2.append(rate[w])

        new_x3 = []
        new_y3 = []

        ddd = 1
        for i in range(ddd, len(new_x2) - ddd):
            if ddd == 0:
                new_x3.append(np.mean(new_x2[i]))
                new_y3.append(np.mean(new_y2[i]))
            else:
                new_x3.append(np.mean(new_x2[i - ddd:i + ddd]))
                new_y3.append(np.mean(new_y2[i - ddd:i + ddd]))

        new_x = []
        new_y = []

        yy = new_y3[6:22]
        xx = new_x3[6:22]

        if splited[-1] == "Shanghai":
            yy = new_y3[6:23]
            xx = new_x3[6:23]

        if splited[-1] == "Beijing":
            yy = new_y3[6:25]
            xx = new_x3[6:25]

        for w in range(len(xx)):
            if yy[w] > 0:
                new_x.append(xx[w])
                new_y.append(yy[w])
        new_y = np.log10(new_y)

        m, bb = np.polyfit(new_x, new_y, 1)
        tau = -1 / m

        plt.semilogy(new_x3[:25], new_y3[:25], 'o', color='white', mec=cm.cool(cl / 2), mew=3, linewidth=2, ms=8,
                     label=splited[-1] + " - China" + r'$, \tau = $' + str(tau)[:4])
        temp = [10 ** (m * xr + bb) for xr in new_x]
        plt.plot(new_x, temp, '--', color=cm.cool(cl / 2), linewidth=3)
        cl = cl + 1

    plt.tick_params(labelsize=25)
    plt.legend(loc='upper right', fontsize=15, ncol=1)
    plt.ylabel(r'$P_{infection}(t)$', fontsize=32)
    plt.xlabel('Days from first infection', fontsize=32)
    plt.xlim([0, 50])
    plt.xticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    plt.ylim([10 ** -3, 10 ** 1])
    plt.tight_layout()


def show_infection_rate_china():

    #load data china
    data = []
    with open('/home/bnaya/Desktop/COVID19/city-confirmed-pivot-day-summary-2020-03-01.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data.append(row)

    data_recovered = [] ## the csv file include also death
    with open('/home/bnaya/Desktop/COVID19/city-D-pivot-day-summary-2020-03-01.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data_recovered.append(row)




    ## cities in Hubei province
    plt.figure(figsize=(10,8))
    cl = 0
    for row in data[1:]:
        splited = row[0].split(',')
        if splited[-6] in ["Wuhan", "Xiaogan",  "Jingzhou"]:
            for row_r in data_recovered[1:]:
                splited_r = row_r[0].split(',')
                if splited_r[-1] == splited[-6]:
                    r = splited_r[53:-2]

            a = [float(s) for s in splited[:39] ]
            b = []



            # calculate rate
            l = 1
            if splited[-6] == "Suizhou":
                for i in range(2+ l -1, len(a)):
                    if len(r[i]) != 0:
                        b.append((a[i] - a[i - 1]) / (a[i - l] - float(r[i - l])))
                    else:
                        b.append((a[i] - a[i - 1]) / a[i - l])
                time = [qq+l for qq in range(1, len(b) + 1)]
            else:
                for i in range(1+ l -1, len(a)):
                    if len(r[i]) != 0:
                        b.append((a[i] - a[i - 1]) / (a[i - l] - float(r[i - l])))
                    else:
                        b.append((a[i] - a[i - 1]) / a[i - l])
                time = [qq+l for qq in range(len(b))]



            new_x2 = []
            new_y2 = []
            for w in range(len(b)):
                if b[w]  > 0:
                    new_x2.append(time[w])
                    new_y2.append(b[w])

            new_x3 = []
            new_y3 = []

            ddd = 1
            for i in range(ddd, len(new_x2)-ddd):
                if ddd == 0:
                    new_x3.append(np.mean(new_x2[i]))
                    new_y3.append(np.mean(new_y2[i]))
                else:
                    new_x3.append(np.mean(new_x2[i - ddd:i + ddd]))
                    new_y3.append(np.mean(new_y2[i - ddd:i + ddd]))

            new_x = []
            new_y = []

            yy = new_y3[6:]
            xx = new_x3[6:]
            if splited[-6] == "Suizhou":
                yy = new_y3[6:]
                xx = new_x3[6:]
            for w in range(len(xx)):
                if yy[w]  > 0:
                    new_x.append(xx[w])
                    new_y.append(yy[w])
            new_y = np.log10(new_y)

            m, bb = np.polyfit(new_x,new_y,1)
            tau = -1/m

            plt.semilogy(new_x3, new_y3, 'o', color='white', mec = cm.cool(cl/2),mew=3, linewidth=2, ms=8, label=splited[-6] + r'$, \tau = $' + str(tau)[:4])

            temp = [10**(m*xr + bb) for xr in new_x]
            plt.plot(new_x, temp, '--', color = cm.cool(cl/2), linewidth = 3)
            cl = cl+1

    plt.xlim([l,len(new_x3)+l + 9])
    ticks = ["2020-01-23"	, "2020-01-24",	"2020-01-25"	,"2020-01-26"	,"2020-01-27",	"2020-01-28"	,"2020-01-29",	"2020-01-30",	"2020-01-31"	,"2020-02-01",	"2020-02-02",	"2020-02-03",	"2020-02-04",	"2020-02-05"	,"2020-02-06"	,"2020-02-07",	"2020-02-08",	"2020-02-09",	"2020-02-10"	,"2020-02-11"	,"2020-02-12"	,"2020-02-13",	"2020-02-14","2020-02-15",	"2020-02-16",	"2020-02-17","2020-02-18","2020-02-19", "2020-02-20", "2020-02-21" ,"2020-02-22", "2020-02-23" ,"2020-02-24", "2020-02-25","2020-02-26" ,"2020-02-27", "2020-02-28", "2020-02-29", "2020-03-01"]
    new_ticks = [ticks[i*3+l] for i in range(int((len(ticks)-l)/3))]
    plt.xticks([i*3+l for i in range(int((len(ticks)-l)/3))],new_ticks, rotation= 45)
    plt.tick_params(labelsize=25)
    plt.legend(loc='upper right', fontsize=18)
    plt.ylim([10**-3, 10**1])
    plt.ylabel(r'$P_{infection}(t)$', fontsize=32)
    plt.xlabel(r'$Time$', fontsize=32)
    plt.tight_layout()


    # small cities in China
    plt.figure(figsize=(10,8))
    cl = 0
    for row in data[1:]:
        splited = row[0].split(',')
        if splited[-6] in ["Hefei", "Xinyang",  "Haerbin"]:
            for row_r in data_recovered[1:]:
                splited_r = row_r[0].split(',')
                if splited_r[-1] == splited[-6]:
                    r = splited_r[53:-2]

            a = [float(s) for s in splited[:39]]
            b = []


            # calculate rate
            l = 1
            for i in range(1+ l -1, len(a)):
                if len(r[i]) != 0:
                    b.append((a[i] - a[i - 1]) / (a[i - l] - float(r[i - l])))
                else:
                    b.append((a[i] - a[i - 1]) / a[i - l])
            time = [qq+l for qq in range(len(b))]


            new_x2 = []
            new_y2 = []
            for w in range(len(b)):
                if b[w]  > 0:
                    new_x2.append(time[w])
                    new_y2.append(b[w])

            new_x3 = []
            new_y3 = []

            ddd = 1
            for i in range(ddd, len(new_x2)-ddd):
                if ddd == 0:
                    new_x3.append(np.mean(new_x2[i]))
                    new_y3.append(np.mean(new_y2[i]))
                else:
                    new_x3.append(np.mean(new_x2[i - ddd:i + ddd]))
                    new_y3.append(np.mean(new_y2[i - ddd:i + ddd]))


            new_x = []
            new_y = []

            yy = new_y3[6:]
            xx = new_x3[6:]

            if splited[-6] == "Bengbu":
                yy = new_y3[6:]
                xx = new_x3[6:]

            for w in range(len(xx)):
                if yy[w]  > 0:
                    new_x.append(xx[w])
                    new_y.append(yy[w])
            new_y = np.log10(new_y)

            m, bb = np.polyfit(new_x,new_y,1)
            tau = -1/m
            plt.semilogy(new_x3, new_y3, 'o', color='white', mec = cm.rainbow(cl/2),mew=3, linewidth=2, ms=8, label=splited[-6] + r'$, \tau = $' + str(tau)[:4])


            temp = [10**(m*xr + bb) for xr in new_x]
            plt.plot(new_x, temp, '--', color = cm.rainbow(cl/2), linewidth = 3)
            cl = cl+1


    plt.xlim([l,len(new_x3)+l + 9])
    ticks = ["2020-01-23"	, "2020-01-24",	"2020-01-25"	,"2020-01-26"	,"2020-01-27",	"2020-01-28"	,"2020-01-29",	"2020-01-30",	"2020-01-31"	,"2020-02-01",	"2020-02-02",	"2020-02-03",	"2020-02-04",	"2020-02-05"	,"2020-02-06"	,"2020-02-07",	"2020-02-08",	"2020-02-09",	"2020-02-10"	,"2020-02-11"	,"2020-02-12"	,"2020-02-13",	"2020-02-14","2020-02-15",	"2020-02-16",	"2020-02-17","2020-02-18","2020-02-19", "2020-02-20", "2020-02-21" ,"2020-02-22", "2020-02-23" ,"2020-02-24", "2020-02-25","2020-02-26" ,"2020-02-27", "2020-02-28", "2020-02-29", "2020-03-01"]
    new_ticks = [ticks[i*3+l] for i in range(int((len(ticks)-l)/3))]
    plt.xticks([i*3+l for i in range(int((len(ticks)-l)/3))],new_ticks, rotation= 45)
    plt.tick_params(labelsize=25)
    plt.ylim([10**-3, 10**1])
    plt.legend(loc='upper right', fontsize=18)
    plt.ylabel(r'$P_{infection}(t)$', fontsize=32)
    plt.xlabel(r'$Time$', fontsize=32)
    plt.tight_layout()
