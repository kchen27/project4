


Burglary = {"+b" : 0.001,
            "-b" : 0.999}

Earthquake = {"+e" : 0.002,
              "-e" : 0.998}

Alarm = {("+b", "+e", "+a") : 0.95,
         ("+b", "+e", "-a") : 0.05,
         ("+b", "-e", "+a") : 0.94,
         ("+b", "-e", "-a") : 0.06,
         ("-b", "+e", "+a") : 0.29,
         ("-b", "+e", "-a") : 0.71,
         ("-b", "-e", "+a") : 0.0001,
         ("-b", "-e", "-a") : 0.999}

John_Calls = {
    ("+a", "+j") : 0.9,
    ("+a", "-j") : 0.1,
    ("-a", "+j") : 0.05,
    ("-a", "-j") : 0.95,
}


Mary_Calls = {
    ("+a", "+m") : 0.7,
    ("+a", "-m") : 0.3,
    ("-a", "+m") : 0.01,
    ("-a", "-m") : 0.99,
}


## Variables to eliminate order: Mary, Alarm, Earthquake

# Initial Factors
# P(A|B,C)
# P(E)
# P(M|A)
# P(J|A)
# P(B)


#First join and eliminate on E
Alarm_eliminate_Earthquake = dict() # proportional to P(A, B)

for entry in Alarm:
    b_val = entry[0]
    e_val = entry[1]
    a_val = entry[2]

    prob_earthquake = Earthquake[e_val]
    prob_alarm = Alarm[entry]

    new_entry = (b_val, a_val)

    # Summing over E
    if new_entry in Alarm_eliminate_Earthquake:
        Alarm_eliminate_Earthquake[new_entry] = Alarm_eliminate_Earthquake[new_entry] + (prob_earthquake * prob_alarm)
    else:
        Alarm_eliminate_Earthquake[new_entry] = (prob_earthquake * prob_alarm)




## Now we join and eliminate on A
John_Calls_Eliminate_Alarm = dict() #P(B, j+)

for entry in Alarm_eliminate_Earthquake:
    prob_alarm = Alarm_eliminate_Earthquake[entry]

    a_val = entry[1]
    b_val = entry[0]

    val_for_john = (a_val, "+j") #Since we want to know +j

    prob_john = John_Calls[val_for_john]

    new_entry = b_val

    if new_entry in John_Calls_Eliminate_Alarm:
        John_Calls_Eliminate_Alarm[new_entry] = John_Calls_Eliminate_Alarm[new_entry] + (prob_alarm * prob_john)
    else:
        John_Calls_Eliminate_Alarm[new_entry] = (prob_alarm * prob_john)


Final_Table = dict()
for entry in John_Calls_Eliminate_Alarm:
    prob_john = John_Calls_Eliminate_Alarm[entry]
    prob_burglary = Burglary[entry]
    Final_Table[entry] = prob_john * prob_burglary


# Now normalize
sum = 0
for entry in Final_Table:
    sum += Final_Table[entry]

for entry in Final_Table:
    Final_Table[entry] = Final_Table[entry]/sum


# Print

print(" B | P(B|+j)")
print("________________________")
for entry in Final_Table:
    print(entry, "|" ,Final_Table[entry])
