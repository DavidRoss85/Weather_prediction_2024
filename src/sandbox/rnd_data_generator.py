from random import randint, random, uniform

filename="../data/fake_data.csv"

#generate some fake data
writefile=open(filename,"w")
temperature=0
humidity=0
precipitation=0.0

writefile.write("Date,Temperature,Humidity,Precipitation")
#Simulate 10 years of data
for _ in range(10):
    for i in range(1,365):
        if 93 <= i < 171:
            temperature=randint(40,80)
        elif 171 <= i < 264:
            temperature=randint(70,110)
        elif 264 <= i < 355:
            temperature=randint(50,80)
        else:
            temperature = randint(20, 50)

        humidity=randint(0,100)
        precipitation=randint(0,100)
        writefile.write(f"\n{i},{temperature},{humidity},{precipitation}")

writefile.close()