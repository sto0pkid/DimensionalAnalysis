from src import Unit


kg = Unit({'kg':1})
m  = Unit({'m':1})
s  = Unit({'s':1})
USD = Unit({'$':1})
year = Unit({'year':1})
day = Unit({'day':1})
hour = Unit({'hour':1})
minute = Unit({'minute':1})

def test():
    print("Test")
    print(Unit())
    print(kg)
    print(m)
    print(s)
    print(kg * m)
    print(kg^2)
    print((kg^2)/kg)
    print(((kg^2)/m)/m)
    print((kg^2)*(m^(-2)))
    print(((kg^2)*(m^(-2)))^(-1))
    print((((kg^2)/m)/m) == ((kg^2)*(m^(-2))))
    print((((kg^2)/m)/m) == (((kg^2)*(m^(-2)))^(-1)))
    print(kg == s)
    print(kg == kg^1)
    print(kg - kg)
    print(kg + kg)
    try:
        print(kg + s)
    except ValueError:
        print("Can't add",kg,"to",s)
    print((m/s) + (m/s))
    print((m/s)^2)
    print(5*(m/s))
    print((5*(m/s)) + (10*(m/s)))
    try:
        print((5*(m/s)) + (10*kg))
    except ValueError:
        print("Can't add",(m/s),"to",kg)
    print((5*(m/s))*(10*kg))
    print((50*USD)/s)
    v = (  (60*s)/minute
         * (60*minute)/hour
         * (24*hour)/day
         * (365*day)/year
        )
    print(v)
    print()
test()
