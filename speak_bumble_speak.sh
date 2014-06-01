#!/bin/bash
# 
# use this script instead of festival on a Mac to make bumble speak 
# we use the glory of netcat to accomplish this task .
#
# relies on the mac command say(1)
# use say -v ? to list all the available voices ...
# on my mac running 1.9.2 the list is :
# 
# timball@thompson {11}$ say -v ?
# Agnes               en_US    # Isn't it nice to have a computer that will talk to you?
# Albert              en_US    #  I have a frog in my throat. No, I mean a real frog!
# Alex                en_US    # Most people recognize me by my voice.
# Bad News            en_US    # The light you see at the end of the tunnel is the headlamp of a fast approaching train.
# Bahh                en_US    # Do not pull the wool over my eyes.
# Bells               en_US    # Time flies when you are having fun.
# Boing               en_US    # Spring has sprung, fall has fell, winter's here and it's colder than usual.
# Bruce               en_US    # I sure like being inside this fancy computer
# Bubbles             en_US    # Pull the plug! I'm drowning!
# Cellos              en_US    # Doo da doo da dum dee dee doodly doo dum dum dum doo da doo da doo da doo da doo da doo da doo
# Deranged            en_US    # I need to go on a really long vacation.
# Fred                en_US    # I sure like being inside this fancy computer
# Good News           en_US    # Congratulations you just won the sweepstakes and you don't have to pay income tax again.
# Hysterical          en_US    # Please stop tickling me!
# Junior              en_US    # My favorite food is pizza.
# Kathy               en_US    # Isn't it nice to have a computer that will talk to you?
# Pipe Organ          en_US    # We must rejoice in this morbid voice.
# Princess            en_US    # When I grow up I'm going to be a scientist.
# Ralph               en_US    # The sum of the squares of the legs of a right triangle is equal to the square of the hypotenuse.
# Trinoids            en_US    # We cannot communicate with these carbon units.
# Vicki               en_US    # Isn't it nice to have a computer that will talk to you?
# Victoria            en_US    # Isn't it nice to have a computer that will talk to you?
# Whisper             en_US    # Pssssst, hey you, Yeah you, Who do ya think I'm talking to, the mouse?
# Zarvox              en_US    # That looks like a peaceful planet.
# 
# --timball@sunlightfoundation.com
# 2014-05-31

while True
do
    nc -l 8888 | say -v "Trinoids"
done
