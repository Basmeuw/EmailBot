import grey_harvest

harvester = grey_harvest.GreyHarvester()

count = 0
for proxy in harvester.run():
    print (proxy)
    count += 1
    if count >= 10:
        break

